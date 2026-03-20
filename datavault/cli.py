"""DataVault CLI — local-first data asset manager."""
import argparse
import sys
from datavault import __version__


def cmd_scan(args):
    """Scan a directory and catalog data assets."""
    from datavault.scanner import scan_directory

    inventory = None
    if args.save:
        from datavault.inventory import Inventory
        inventory = Inventory()

    results = scan_directory(
        args.path,
        recursive=not args.no_recursive,
        skip_privacy=args.skip_privacy,
        save=args.save,
        inventory=inventory,
    )
    print(f"Scanned {results['total']} files in {args.path}")
    for cat, count in sorted(results["categories"].items()):
        print(f"  {cat}: {count}")

    risk = results.get("risk_summary", {})
    if risk and set(risk.keys()) != {"safe"}:
        print("\nPrivacy risks detected:")
        for level, count in sorted(risk.items()):
            if level != "safe":
                print(f"  {level}: {count}")

    if inventory is not None:
        inventory.close()


def cmd_classify(args):
    """Classify a single file or directory."""
    from datavault.classifier import classify_path
    info = classify_path(args.path)
    print(f"{args.path} → {info['category']} ({info['mime']})")


def cmd_report(args):
    """Generate a summary report of data assets."""
    from datavault.scanner import scan_directory
    from datavault.reporter import generate_report
    results = scan_directory(args.path, recursive=True)
    report = generate_report(results, fmt=args.format)
    print(report)


def cmd_search(args):
    """Search the asset inventory."""
    from datavault.inventory import Inventory
    inv = Inventory()
    results = inv.search(query=args.query, category=args.category, risk=args.risk)
    inv.close()
    if not results:
        print("No matching assets found.")
        return
    for r in results:
        print(f"  {r['path']}  [{r['category']}]  risk={r['privacy_risk']}")


def cmd_stats(args):
    """Show inventory statistics."""
    from datavault.inventory import Inventory
    inv = Inventory()
    s = inv.stats()
    inv.close()
    print(f"Total assets: {s['total']}")
    if s["categories"]:
        print("Categories:")
        for cat, count in sorted(s["categories"].items()):
            print(f"  {cat}: {count}")
    if s["risk_summary"]:
        print("Risk summary:")
        for risk, count in sorted(s["risk_summary"].items()):
            print(f"  {risk}: {count}")


def cmd_privacy(args):
    """Run privacy detection on a file or directory."""
    import os
    from datavault.privacy import PrivacyDetector
    detector = PrivacyDetector()

    if os.path.isfile(args.path):
        targets = [args.path]
    elif os.path.isdir(args.path):
        targets = []
        for root, dirs, filenames in os.walk(args.path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for fname in filenames:
                if not fname.startswith("."):
                    targets.append(os.path.join(root, fname))
    else:
        print(f"Path not found: {args.path}")
        sys.exit(1)

    found_any = False
    for fpath in targets:
        findings = detector.scan_file(fpath)
        risk = detector.risk_level(findings)
        if risk != "safe":
            found_any = True
            print(f"  [{risk:8s}] {fpath}")
            for item in findings["findings"]:
                print(f"           {item['type']}: {item['count']} occurrence(s)")

    if not found_any:
        print("No sensitive information detected.")


def cmd_register(args):
    """Register asset(s) to Oasyce."""
    from datavault.bridge import OasyceBridge
    bridge = OasyceBridge()
    if not bridge.check_oasyce_available():
        print("oasyce_plugin not installed. Run: pip install datavault[oasyce]")
        sys.exit(1)
    tags = args.tags.split(",") if args.tags else []
    result = bridge.register_asset(args.path, owner=args.owner, tags=tags)
    if result["success"]:
        print(f"Registered: {args.path} → {result.get('asset_id', 'ok')}")
    else:
        print(f"Failed: {result['error']}")


def cmd_version(_args):
    print(f"datavault {__version__}")


def main():
    parser = argparse.ArgumentParser(
        prog="datavault",
        description="Local-first data asset manager",
    )
    sub = parser.add_subparsers(dest="command")

    # scan
    p_scan = sub.add_parser("scan", help="Scan directory for data assets")
    p_scan.add_argument("path", nargs="?", default=".")
    p_scan.add_argument("--no-recursive", action="store_true")
    p_scan.add_argument("--skip-privacy", action="store_true",
                        help="Skip privacy detection for faster scanning")
    p_scan.add_argument("--save", action="store_true",
                        help="Save results to local inventory")
    p_scan.set_defaults(func=cmd_scan)

    # classify
    p_cls = sub.add_parser("classify", help="Classify a file")
    p_cls.add_argument("path")
    p_cls.set_defaults(func=cmd_classify)

    # report
    p_rpt = sub.add_parser("report", help="Generate asset report")
    p_rpt.add_argument("path", nargs="?", default=".")
    p_rpt.add_argument("--format", choices=["text", "json", "markdown"],
                       default="text")
    p_rpt.set_defaults(func=cmd_report)

    # search
    p_search = sub.add_parser("search", help="Search asset inventory")
    p_search.add_argument("query", nargs="?", default="")
    p_search.add_argument("--category", default="")
    p_search.add_argument("--risk", default="")
    p_search.set_defaults(func=cmd_search)

    # stats
    sub.add_parser("stats", help="Show inventory statistics").set_defaults(
        func=cmd_stats
    )

    # privacy
    p_priv = sub.add_parser("privacy", help="Run privacy detection")
    p_priv.add_argument("path")
    p_priv.set_defaults(func=cmd_privacy)

    # register (Oasyce bridge)
    p_reg = sub.add_parser("register", help="Register asset to Oasyce")
    p_reg.add_argument("path")
    p_reg.add_argument("--owner", required=True)
    p_reg.add_argument("--tags", default="")
    p_reg.add_argument(
        "--confirm", action="store_true", required=True,
        help="Confirm registration (prevents accidental uploads)"
    )
    p_reg.set_defaults(func=cmd_register)

    # version
    sub.add_parser("version", help="Show version").set_defaults(func=cmd_version)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
