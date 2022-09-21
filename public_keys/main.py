import dearpygui.dearpygui as dpg
from eth_account import Account

dpg.create_context()


def fetch_rawtx(sender, app_data):
    account = Account()
    pubkeys = []
    file_path_name = app_data["file_path_name"]
    with open(file_path_name, "r", encoding="utf-8") as f:
        rawtx_list = f.readlines()

    for rawtx in rawtx_list:
        pubkey = account.recover_transaction(rawtx.strip())
        pubkeys.append(str(pubkey))

    with open("output.txt", "w", encoding="utf-8") as f:
        for pubkey in pubkeys:
            f.write(pubkey + "\n")


with dpg.file_dialog(directory_selector=True,
                     show=False,
                     callback=fetch_rawtx,
                     tag="file_dialog_id"):
    dpg.add_file_extension(".txt")
    dpg.add_file_extension(".json")

with dpg.window(label="Upload File with rawTx", width=600, height=250):
    dpg.add_button(label="Upload",
                   callback=lambda: dpg.show_item("file_dialog_id"))

dpg.create_viewport(title="Public Keys Extractor", width=600, height=250)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
