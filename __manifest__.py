{
    "name": "Fleetra",
    "version": "1.0.0",
    "category": "Operations/Fleet",
    "summary": "Smart Fleet. Smarter Moves.",
    "author": "Shruti Rai",
    "license": "LGPL-3",

    "depends": [
        "base",
        "web",
    ],

    "data": [
        "security/ir.model.access.csv",
        "data/demo_data.xml",
        "views/vehicle_views.xml",
        "views/driver_views.xml",
        "views/trip_views.xml",
        "views/menu_views.xml",
    ],

    "application": True,
    "installable": True,
    "auto_install": False,
}