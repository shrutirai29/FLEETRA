{
    "name": "Fleetra",
    "version": "1.0.0",
    "category": "Operations/Fleet",
    "summary": "Smart Fleet. Smarter Moves.",
    "description": """
Fleetra is a smart transport operations platform for managing
vehicles, drivers, trips, maintenance, fuel, expenses and fleet analytics.
    """,
    "author": "Shruti Rai",
    "license": "LGPL-3",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",

        "views/vehicle_views.xml",
        "views/driver_views.xml",
        "views/trip_views.xml",
        "views/maintenance_views.xml",
        "views/fuel_views.xml",
        "views/expense_views.xml",
        "views/menu_views.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}