{
    "name": "Fleetra",
    "version": "19.0.1.0.0",
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
        "views/dashboard_views.xml",
        "views/vehicle_views.xml",
        "views/driver_views.xml",
        "views/trip_views.xml",
        "views/maintenance_views.xml",
        "views/fuel_views.xml",
        "views/expense_views.xml",
        "views/menu_views.xml",
    ],

    "assets": {
        "web.assets_backend": [
            "FLEETRA/static/src/js/dashboard.js",
            "FLEETRA/static/src/xml/dashboard.xml",
            "FLEETRA/static/src/scss/dashboard.scss",
        ],
    },

    "application": True,
    "installable": True,
    "auto_install": False,
}