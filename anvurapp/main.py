import re
from functools import partial
from tinydb import TinyDB, Query
import flet as ft
from process_scimago import get_scimago_data


def main(page):
    # List of fields from Scimago for display
    scimago_fields = ["Rank", "SJR", "H index"]
    # Database components
    db = TinyDB('db.json')
    anvur = db.table('anvur')
    classea = db.table('classea')
    scientific = db.table('scientific')
    scimago_db = TinyDB('scimago.json')
    scimago = scimago_db.table('scimago')
    Journal = Query()
    # Page components
    txt_search = ft.TextField(label="Journal name")
    lv = ft.ListView(expand=True, spacing=10)
    details = ft.Column()

    def on_keyboard(e: ft.KeyboardEvent):
        #print(e.key)
        if e.key == "Enter":
            search_click(e)
        if e.key == "Escape":
            details_clear(e)

    def details_clear(e):
        details.controls = []
        page.update()

    def details_click(e, issn, title):
        """Function to populate journal details"""
        # Clear previous details
        details.controls = []
        # Journal title and ISSN
        details.controls.append(ft.Text(title, size=30, weight=ft.FontWeight.BOLD))
        details.controls.append(ft.Text(f"ISSN: {issn}", size=15))
        search_results = []
        # Scientific sectors
        scientific_details = scientific.search(Journal.ISSN == issn)
        if len(scientific_details) == 1:
            scientific_column = []
            scientific_column.append(ft.Text("Scientific sectors", size=20, weight=ft.FontWeight.BOLD))
            # Get dict inside list and pop ISSN
            scientific_listview = ft.ListView(expand=True, spacing=5)
            scientific_details = {k:v for k,v in scientific_details[0].items() if k != "ISSN"}
            for k, v in scientific_details.items():
                scientific_listview.controls.append(
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 3}, controls=[ft.Text(k)]),
                        ft.Column(col={"sm": 3}, controls=[ft.Text(v)]),
                    ])
                )
            scientific_column.append(scientific_listview)
            search_results.append(scientific_column)
        # Classe A
        classea_details = classea.search(Journal.ISSN == issn)
        if len(classea_details) == 1:
            classea_column = []
            classea_column.append(ft.Text("Classe A", size=20, weight=ft.FontWeight.BOLD))
            # Get dict inside list and pop ISSN
            classea_listview = ft.ListView(expand=True, spacing=5)
            classea_details = {k:v for k,v in classea_details[0].items() if k != "ISSN"}
            for k, v in classea_details.items():
                classea_listview.controls.append(
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 3}, controls=[ft.Text(k)]),
                        ft.Column(col={"sm": 3}, controls=[ft.Text(v)]),
                    ])
                )
            classea_column.append(classea_listview)
            search_results.append(classea_column)
        # Scimago details
        scimago_details = scimago.search(Journal.ISSN == issn)
        if len(scimago_details) == 1:
            scimago_column = []
            scimago_column.append(ft.Text("Scimago JR", size=20, weight=ft.FontWeight.BOLD))
            # link in Button
            scimago_button = ft.ElevatedButton("View on Scimago JR", url=scimago_details[0].get("Link"))
            # Get dict inside list and pop ISSN
            scimago_listview = ft.ListView(expand=True, spacing=5)
            scimago_details = {k:v for k,v in scimago_details[0].items() if k in scimago_fields}
            for k, v in scimago_details.items():
                scimago_listview.controls.append(
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 3}, controls=[ft.Text(k)]),
                        ft.Column(col={"sm": 3}, controls=[ft.Text(v)]),
                    ])
                )
            scimago_column.append(scimago_listview)
            scimago_column.append(scimago_button)
            search_results.append(scimago_column)
        # Append all results to details as separate columns
        details.controls.append(
            ft.ResponsiveRow([
                ft.Column(col=4, controls=res)
                for res in search_results
            ])
        )
        details.controls.append(ft.Text("Notes: ‡(year) means included until 31.12.year; S/A(year) means included from 01.01.year", size = 10))
        details.controls.append(ft.ElevatedButton("Clear details", on_click=details_clear))
        page.update()

    def search_click(e):
        if not txt_search.value:
            txt_search.error_text = "Please enter a journal name"
            page.update()
        else:
            fragment = txt_search.value
            # Search journal
            
            results = anvur.search(Journal.TITOLO.search(f"{fragment}+", flags=re.IGNORECASE))
            # Remove previous results
            lv.controls = []
            for res in results:
                lv.controls.append(ft.ResponsiveRow([
                    ft.Column(col={"sm": 5}, controls=[ft.Text(res.get("TITOLO"))]),
                    ft.Column(col={"sm": 4}, controls=[ft.Text("ISSN: {}".format(res.get("ISSN")))]),
                    ft.Column(col={"sm": 3}, controls=[ft.ElevatedButton(
                        "Details", on_click=partial(details_click, issn=res.get("ISSN"), title=res.get("TITOLO")))])
                ]))
            page.update()
    
    def update_scimago(e):
        """Function to download data from Scimago JR"""
        progress = ft.AlertDialog(
            title = ft.ProgressBar(width=400)
        )
        page.open(progress)
        result = get_scimago_data()
        alert = ft.AlertDialog(
            title=ft.Text(result)
        )
        page.open(alert)

    def update_anvur(e):
        """Function to download Anvur data from server"""
        progress = ft.AlertDialog(
            title = ft.ProgressBar(width=400)
        )
        page.open(progress)
        result = get_anvur_data()
        alert = ft.AlertDialog(
            title=ft.Text(result)
        )
        page.open(alert)
    
    # Add keyboard shortcuts
    page.on_keyboard_event = on_keyboard
    # Build layout
    page.add(
        ft.ResponsiveRow([
            ft.Column(col={"sm": 6}, controls=[ft.Text("ANVUR Journal search",size=50, weight=ft.FontWeight.BOLD)]),
            ft.Column(col={"sm": 3}, controls=[ft.ElevatedButton("Update Anvur")]),
            ft.Column(col={"sm": 3}, controls=[ft.ElevatedButton("Update Scimago JR", on_click=update_scimago)]),
        ]),
        
        txt_search, 
        ft.ElevatedButton("Search", on_click=search_click),
        details,
        lv
        )
    # Make the page scrollable
    page.scroll = ft.ScrollMode.ADAPTIVE

ft.app(main)
