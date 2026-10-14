"""School bus transport register.

Enrols riders onto bus routes, reports route rosters, sends dispatch
alerts and totals the fees collected for each route.
"""

import logging
import sqlite3
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE riders ("
    "id INTEGER PRIMARY KEY, "
    "student TEXT, route TEXT, stop TEXT, fee INTEGER)"
)


def enrol_rider(student, route, stop, fee):
    """Insert a rider using a parameterised query."""
    conn.execute(
        "INSERT INTO riders (student, route, stop, fee) "
        "VALUES (?, ?, ?, ?)",
        (student, route, stop, fee),
    )
    conn.commit()


def route_roster(route):
    """Return the names of the riders assigned to a route."""
    cursor = conn.execute(
        "SELECT student FROM riders WHERE route = ?",
        (route,),
    )
    return [row[0] for row in cursor]


def export_roster(path, route):
    """Write a route roster to a text file, one name per line."""
    with open(path, "w", encoding="utf-8") as out:
        for name in route_roster(route):
            out.write(name + "\n")


def dispatch_alert(route):
    """Send a dispatch message without invoking a shell."""
    subprocess.run(
        ["echo", "dispatching bus", route],
        check=False,
    )


def fee_collected(route):
    """Return the total fee for a route, or 0 if the query fails."""
    try:
        row = conn.execute(
            "SELECT SUM(fee) FROM riders WHERE route = ?",
            (route,),
        ).fetchone()
        return row[0]
    except sqlite3.Error:
        logger.exception("could not total fees for route %s", route)
        return 0


def main():
    """Run a short demonstration of the register."""
    enrol_rider("Tara", "R1", "Lake Road", 1800)
    enrol_rider("Kabir", "R1", "Mill Street", 1800)
    enrol_rider("Zoya", "R2", "Fort Gate", 2100)

    if fee_collected("R1") != 3600:
        raise RuntimeError("R1 fee total mismatch")

    export_roster("route_r1.txt", "R1")
    dispatch_alert("R1")
    print(route_roster("R2"))


if __name__ == "__main__":
    main()
