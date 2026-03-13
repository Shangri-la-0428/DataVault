"""DataVault CLI — local-first data asset manager."""
import argparse
import sys
from datavault import __version__


def cmd_scan(args):
    """Scan a directory and catalog data assets."""
    from datavault.scanner import scan_directory
    results = scan_directory(args.path, recursive=not args.no_recursive)
    print(f"Scanned {results['total']} files in {args.path}")
    for cat, count in sorted(results["categories"].items()):
        print(f"  {cat}: {count}")


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
    p_scan.set_defaults(func=cmd_scan)

    # classify
    p_cls = sub.add_parser("classify", help="Classify a file")
    p_cls.add_argument("path")
    p_cls.set_defaults(func=cmd_classify)

    # report
    p_rpt = sub.add_parser("report", help="Generate asset report")
    p_rpt.add_argument("path", nargs="?", default=".")
    p_rpt.add_argument("--format", choices=["text", "json"], default="text")
    p_rpt.set_defaults(func=cmd_report)

    # version
    sub.add_parser("version", help="Show version").set_defaults(func=cmd_version)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
