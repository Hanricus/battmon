import sys
if sys.platform != "win32":
    print("battmon by Shakir only runs on Windows.")
    sys.exit()

import ctypes, ctypes.wintypes, time, csv, os, re, subprocess, threading, json, webbrowser
import tempfile
import urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import html as _html
from collections import deque, Counter
from datetime import datetime

# ================= INFO =================
VERSION = "1.1.0"
REPO = "Hanricus/battmon"          # change if your repo name is different
LINKEDIN = "https://www.linkedin.com/in/abdulshakirhakim/"
GITHUB = "https://github.com/Hanricus"
UPDATE_EVERY = 3600                 # seconds, check for updates every hour

# Logo: paste base64 PNG here (run make_logo.py to get it). Empty = default icon.
LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAGpElEQVR42p2Wa4xV5RWGn/XtfeYCFIpcFW3HOIeBAUGDo3ODzU00BRvb5tREa4uNlDT+ofwgvfwgJDVtf1T6owkJUeOlNE3GptXSoBBtj1yUIiraDiBYgRRw5CYiDOfs/X1vf+zDMOC0Nd3JTs7e+6zvXd+71veu1xjiEhiUnNHjATRr4SguXLyNTLdDuAmzUZg8uHNgHxDbbsZes9PKz3+cx5ci6AkGunptGwrs0h81M2mikj2I94uQFTA7AjqK2RkiC3h9EekGHJOQeQiv0lj/hO0pH7p6rSEBBc4gaPVqx++2PIIPy3H2PpH9lga22ls7jg3JyIw7x5Oen4fnPoJuJI6e5b4Fv7I1a8KlNT8DOADWvXg0x06vw9FM7B61/Tv+gHRFUlCqxbXKWBMup2+oZfbXCdkqzA4wsmGF7Xr51NWgtZqB2hddo+auTSp2Pa+Z8ydd/l6KNAT9g+PzutWe274yUS0df1Rz15/VvuiawRhW+2G0lmLSo8+C1dMy+n7buPGCSGIo+xoV4nNcohQZPV5Llgxj/5mnUfDUXf9telszWCPEagegyd2rNLlzpxbcOwZAra11upLyK3eRJ+tq91W9MKuQd3cyVsXO7ZrcuSp/n2Ohm+e1qNixT1OThfmHJB4InvW9gkqlOv7PSzNmz1ex811N6Z480DQqdq7F3Hh7b9sDA5S0JneTpvcgjUMynJ0krnuJveXnDaRpc9qo+odAImp4wva98mbOTDKCLPshPkwkpsf2v/aSit0bQH12YPtKp7ZkIqIT557Kz02P15TuZVysrCX1cwlhBtJ0Us2hUvkZLV0rAUjDJDLdSRbm4ysrlCRxTm19HZm6CboLXJPAqIufwaxDrclExzk/F1k/N9TvMJBmdIzHh/sR54nityhEq6iPV1JwO/GqkPrvaub8SZg+xtSPdJwsu5U+f7eBCN6w8CnYWXAVAzFW21G4SPBzHZnacDpoW7acB6BQmIBXA1BPXeFPtn/HC7Z3+yYa3c8pxIdw7jDOX0sIAYjACogKWbZMSdJAVkiRRaCBBrNy+VPMDuB1uwPdiHP/HKhyHH+EWYbUT1p9UC2zl+rmeS18bcFBO7j9XiYVvsqbf92NRcMAjwMiLuJppq/yTQ5sOgc4wJDPBonCIWRNDmMk6FTekbMKtvOVPuqip4hsBN43UU1Xcb7/STZs2aCWruWkoxrNTETBIcVAP4V4B6hKat9i5sIi2AUMywVmAPEUhFF5JqZcdnaPEIDt3foEjfH3KcQv49y/wEbgwwyqfgUnTj+u9lIjsjQ/jjTQWP8bIvceXpO4WHkYIyMYyNxlwAAGMS58guJx+cvxUpLEVMYX7PWeMlBWWzKRc24GIf0GqZ9G5m/l7PG7iOwEGBgFUvqoj5/EVx/Dp53IPEaKGywIGoNx1oE7hNSUH8oezymWcPL4Cyp2bdK0OVNtV/lD2/eXzXy5aSXOMlCK50Ykq+lNwGcj+cfWzUTRHjyNhCF0V+5LGIcd5nYimtWajMh3Ho4RsuvI/AQq/geakrRr6rxpHPngYYJiRIxzhwnyoIDMEyJnIArxOhwOw2MWQLmwJMkI5CeD7XIMH16G0IilbQKjtPUNClEPZsPwvoNqdR3V/qep+mUQxhC7AzjbjDQSVA9qxNJa7V/dSuy2Io2HUE8IuRj0hU7EcBp82dnul46DvU7GQwZiDTAx/ikN0S+I3LtYOIk4R8T7FKLnGN6w3HrLn+LifqL4XeJoH1aoDFBXGL6OOH6HyO0lspM1MViKs7/ZnteP5vTeOmeqiu1/1/S5yWVPApJMs5KxmjL7Ws1aMuwz81MySZ+tl4GS1TGAWjrn6ab2XrV2tzJ4ZGhK149U7HxN3YtHXxpPQwxa998G8aCxlSfcvXi0iu3bVez+yaV4B2skcDR94TGMY3x05nG1lxqtt7cqckG+dBuE/z2IS87Aq1RqpO/Uesz6uC76ZW5NarEDFN1y9zjd1LFZzZ2/1x33TBg8eD+PxbhinWLHc2ru2KI75k+47IWGMlFtC8Zwpv/XKDTRED9qvds2Dt5TXoLeQeCD/KeBWmYvxqc/BneU4SMfsbdfPDHYRA1tE5Mk5sPqCoK+A+wjjjcwLNpmu8snh9xh24IxnO3vRnoAqRXnnmHu9LW2fn36H23ikEb4ljlFLqRLCcypEXcE7AhwujYBRhPC9UATwhG5Mg3R0/bOtvc+lxG+qu3tUmZqWzCGc9V2gm4jZE2g0bXQTzAO4dwbNI58zd5+8cSgemmoBvs3GmIyWnrlE5UAAAAASUVORK5CYII="

FROZEN = getattr(sys, "frozen", False)
SELF = sys.executable if FROZEN else os.path.abspath(__file__)
BIOS_NS = "root\\dcim\\sysman\\biosattributes"
PW_NS = "root\\dcim\\sysman\\wmisecurity"

LOG = os.path.join(os.path.expanduser("~"), "battlog.csv")
CFG_FILE = os.path.join(os.path.expanduser("~"), ".battmon.json")
INTERVAL = 5          # seconds, refresh display
LOG_EVERY = 60        # seconds, write to log file

# ================= LANGUAGE =================
STR = {
    "en": {
        "st_batt": "On battery", "st_charging": "Charging", "st_slow": "Trickle charging",
        "st_hold": "Cutoff / hold (AC only)",
        "f_volt": "Voltage", "f_rate": "Charge / discharge rate", "f_left": "Time left",
        "f_cap": "Current capacity", "f_full": "Full charge", "f_design": "Design capacity",
        "f_health": "Battery health", "f_cycles": "Cycle count", "f_mode": "BIOS mode",
        "f_limit": "Stops / starts at",
        "charge_mode": "CHARGE MODE", "limit": "Charge limit",
        "btn_Standard": "Full", "btn_PrimAcUse": "Hold AC", "btn_Custom": "Custom",
        "tip_Standard": "Full: charges to 100% and stops when full. While plugged in it stays at 100%. Good if you often run on battery.",
        "tip_PrimAcUse": "Hold AC: a Dell mode for laptops that stay plugged in. It reduces full charging, but Dell does not publish the exact limit. For a fixed limit, use Custom.",
        "tip_Custom": "Custom: charging stops at the limit you pick (for example 80%). After that the laptop runs on AC. If you plug in above the limit it will not charge and the level stays put.",
        "ex_full": "Full: charges to 100%, then stays at 100% while plugged in.",
        "ex_hold": "Hold AC: Dell limits full charging for laptops that stay plugged in. The exact limit is not published.",
        "ex_batt": "Limit {b}%. When you plug in, it charges up to {b}% only, then cuts off.",
        "ex_nocharge": "Limit {b}%. At {pct}% it will not charge. The laptop runs straight from AC.",
        "ex_charge": "Limit {b}%. Below {a}%, it charges up to {b}% then cuts off.",
        "applying": "Applying...", "wait": "Please wait, still applying...",
        "ok": "Done. BIOS updated.",
        "fail": "BIOS did not accept it. Current: {mode} {start}-{stop}  ({out})",
        "fail_hint": " The BIOS may have an admin password or an IT policy.",
        "num_err": "Limit must be a number",
        "note_other": "Monitor-only mode. This is a {brand} laptop. Charge limit control only supports Dell for now. Open the battery report for where to find your brand's own tool.",
        "note_nobios": "Monitor-only mode. This Dell BIOS does not expose charge controls, or the app has no admin access.",
        "note_pw": "A BIOS admin password is set. Changing the charge limit will fail unless IT unlocks it.",
        "no_battery": "No battery found on this machine.\n\nwhy we still here just to suffer hahahaha\n\n(Desktop PC? No battery, nothing to control.)",
        "upd_q": "Update battmon from v{cur} to {tag}?\n\nThe new file is downloaded from github.com/{repo}.\nThe old file is kept as battmon.pyw.bak.",
        "upd_fail": "Update failed: {err}",
        "upd_bad": "invalid update file",
        "banner": "⬆ Update {tag} available. Click to update",
        "banner_exe": "⬆ Update {tag} available. Click to open the download page",
        "tray_open": "Open battmon", "tray_exit": "Exit",
        "tray_ask": "battmon needs two small packages (pystray and pillow) so the close button keeps it running in the tray instead of quitting.\n\nInstall them now?",
        "tray_fail": "Could not install tray support. Closing the window will quit battmon.\n\nYou can install it yourself later: pip install pystray pillow",
        "close_quit": "Tray support is not installed, so closing will quit battmon. Quit now?",
        "h_min": "{h} h {m} min",
        # report
        "check": "Battery report", "rep_win_title": "battmon - battery report",
        "rep_title": "battmon battery report", "loading": "Collecting battery data...",
        "sec_laptop": "LAPTOP", "sec_charge": "CHARGE CUTOFF / BYPASS",
        "sec_observed": "OBSERVED BEHAVIOUR (battmon log)", "sec_notes": "NOTES",
        "l_maker": "Manufacturer", "l_model": "Model", "l_bios": "BIOS version", "l_biosdate": "BIOS date",
        "l_admin": "Admin rights", "l_tray": "Tray support (close button keeps it running)",
        "l_battery_n": "BATTERY {n}", "l_id": "Name / ID", "l_chem": "Chemistry",
        "l_serial": "Serial (masked)", "l_mfgdate": "Manufacture date", "l_now": "Charge now",
        "l_verdict": "Health verdict",
        "nr": "not reported", "yes": "yes", "no": "no",
        "v_good": "good (80% or more)", "v_worn": "worn (60 to 79%)",
        "v_weak": "weak (below 60%), consider replacing",
        "mfg_note": "Many laptops do not report the battery manufacture date. The BIOS date above is the laptop's firmware date, not the battery's age. Health verdict is a rough guide only.",
        "charge_dell_ok": "Supported. battmon can set a cutoff limit (50, 80 or 90%) on this Dell through the BIOS.",
        "charge_dell_modes": "Dell BIOS charge modes (Full, Hold AC) are available. A custom limit is not offered on this model.",
        "charge_dell_no": "This is a Dell, but the BIOS charge interface is not available (or the app has no admin access).",
        "charge_vendor": "Many {name} models offer a charge limit (cutoff) through a vendor tool or the BIOS. It depends on the exact model. battmon cannot control it yet.",
        "charge_unknown": "No known charge limit tool for this brand. Check the manufacturer's PC app or the BIOS power/battery page. Windows itself has no charge limit setting.",
        "bypass_note": "True bypass (battery fully taken out of the power path) is rare, mostly on some gaming laptops, and battmon cannot detect it. If your vendor tool offers 'bypass', that is it.",
        "guide": "Where to look: ",
        "tool_found": "Vendor tool found on this PC: {v}",
        "tool_missing": "Vendor tool not found on this PC (looked for: {v}).",
        "obs_none": "Not enough data yet. Leave battmon running while plugged in.",
        "obs_range": "Log range: {a} to {b}. Lowest {lo}%, highest {hi}%.",
        "obs_hold": "On AC it held at {p}% ({n} samples). That looks like a charge cutoff.",
        "obs_full": "On AC it held at 100% ({n} samples). Normal full charge, no cutoff seen yet.",
        "gen": "Generated {t} by battmon v{v}",
        "btn_save": "Save report", "btn_store": "Find vendor tool", "btn_close": "Close",
        "saved": "Report saved:\n{p}", "save_fail": "Could not save: {err}",
    },
    "ms": {
        "st_batt": "Guna bateri", "st_charging": "Sedang mengecas", "st_slow": "Cas perlahan",
        "st_hold": "Cutoff / hold (AC sahaja)",
        "f_volt": "Voltan", "f_rate": "Kadar cas / nyahcas", "f_left": "Baki masa",
        "f_cap": "Kapasiti semasa", "f_full": "Cas penuh", "f_design": "Kapasiti reka bentuk",
        "f_health": "Kesihatan bateri", "f_cycles": "Kiraan kitaran", "f_mode": "Mod BIOS",
        "f_limit": "Berhenti / mula cas",
        "charge_mode": "MOD CAS", "limit": "Had cas",
        "btn_Standard": "Penuh", "btn_PrimAcUse": "Hold AC", "btn_Custom": "Custom",
        "tip_Standard": "Penuh: cas sampai 100% dan berhenti bila penuh. Selagi dipalam ke AC, ia kekal 100%. Sesuai kalau kerap guna bateri.",
        "tip_PrimAcUse": "Hold AC: mod Dell untuk laptop yang sentiasa dipalam. Ia kurangkan cas penuh, tetapi had tepat tidak diumumkan Dell. Untuk had tetap, guna Custom.",
        "tip_Custom": "Custom: cas berhenti pada had yang dipilih (contoh 80%). Selepas itu laptop guna AC terus. Kalau dipalam ketika paras sudah melebihi had, ia tidak mengecas dan paras kekal.",
        "ex_full": "Penuh: cas sampai 100%, kemudian kekal 100% selagi dipalam.",
        "ex_hold": "Hold AC: Dell hadkan cas penuh untuk laptop yang sentiasa dipalam. Had tepat tidak diumumkan.",
        "ex_batt": "Had {b}%. Bila dipalam, ia cas sehingga {b}% sahaja, kemudian cutoff.",
        "ex_nocharge": "Had {b}%. Pada {pct}% ia tidak mengecas. Laptop guna AC terus.",
        "ex_charge": "Had {b}%. Bawah {a}%, ia cas sehingga {b}% kemudian cutoff.",
        "applying": "Sedang apply...", "wait": "Sila tunggu, masih apply...",
        "ok": "Berjaya. BIOS sudah ditukar.",
        "fail": "BIOS tidak terima. Sekarang: {mode} {start}-{stop}  ({out})",
        "fail_hint": " BIOS mungkin ada password admin atau polisi IT.",
        "num_err": "Had mesti nombor",
        "note_other": "Mod monitor sahaja. Ini laptop {brand}. Kawalan had cas hanya sokong Dell buat masa ini. Buka laporan bateri untuk tahu di mana nak cari tool jenama anda.",
        "note_nobios": "Mod monitor sahaja. BIOS Dell ini tidak dedahkan kawalan cas, atau app tiada akses admin.",
        "note_pw": "Password admin BIOS ditetapkan. Menukar had cas akan gagal kecuali IT buka kunci.",
        "no_battery": "Tiada bateri dijumpai pada mesin ini.\n\nwhy we still here just to suffer hahahaha\n\n(PC desktop? Tiada bateri, tiada apa nak dikawal.)",
        "upd_q": "Kemas kini battmon dari v{cur} ke {tag}?\n\nFail baharu dimuat turun dari github.com/{repo}.\nFail lama disimpan sebagai battmon.pyw.bak.",
        "upd_fail": "Kemas kini gagal: {err}",
        "upd_bad": "fail kemas kini tidak sah",
        "banner": "⬆ Kemas kini {tag} tersedia. Klik untuk kemas kini",
        "banner_exe": "⬆ Kemas kini {tag} tersedia. Klik untuk buka laman muat turun",
        "tray_open": "Buka battmon", "tray_exit": "Keluar",
        "tray_ask": "battmon perlukan dua pakej kecil (pystray dan pillow) supaya butang tutup sorok app ke tray dan bukan menutupnya.\n\nPasang sekarang?",
        "tray_fail": "Gagal memasang sokongan tray. Menutup tetingkap akan menutup battmon.\n\nAnda boleh pasang sendiri kemudian: pip install pystray pillow",
        "close_quit": "Sokongan tray tidak dipasang, jadi menutup akan menutup battmon. Keluar sekarang?",
        "h_min": "{h} j {m} min",
        # report
        "check": "Laporan bateri", "rep_win_title": "battmon - laporan bateri",
        "rep_title": "Laporan bateri battmon", "loading": "Mengumpul data bateri...",
        "sec_laptop": "LAPTOP", "sec_charge": "CUTOFF / BYPASS CAS",
        "sec_observed": "KELAKUAN DIPERHATI (log battmon)", "sec_notes": "NOTA",
        "l_maker": "Pengeluar", "l_model": "Model", "l_bios": "Versi BIOS", "l_biosdate": "Tarikh BIOS",
        "l_admin": "Hak admin", "l_tray": "Sokongan tray (butang tutup kekalkan app berjalan)",
        "l_battery_n": "BATERI {n}", "l_id": "Nama / ID", "l_chem": "Kimia",
        "l_serial": "Siri (disorok)", "l_mfgdate": "Tarikh dibuat", "l_now": "Cas sekarang",
        "l_verdict": "Penilaian kesihatan",
        "nr": "tidak dilaporkan", "yes": "ya", "no": "tidak",
        "v_good": "baik (80% ke atas)", "v_worn": "haus (60 hingga 79%)",
        "v_weak": "lemah (bawah 60%), pertimbang tukar",
        "mfg_note": "Kebanyakan laptop tidak melaporkan tarikh bateri dibuat. Tarikh BIOS di atas ialah tarikh firmware laptop, bukan umur bateri. Penilaian kesihatan hanyalah panduan kasar.",
        "charge_dell_ok": "Disokong. battmon boleh tetapkan had cutoff (50, 80 atau 90%) pada Dell ini melalui BIOS.",
        "charge_dell_modes": "Mod cas BIOS Dell (Penuh, Hold AC) tersedia. Had custom tidak ditawarkan pada model ini.",
        "charge_dell_no": "Ini Dell, tetapi antara muka cas BIOS tidak tersedia (atau app tiada akses admin).",
        "charge_vendor": "Banyak model {name} menawarkan had cas (cutoff) melalui tool pengeluar atau BIOS. Ia bergantung pada model tepat. battmon belum boleh mengawalnya.",
        "charge_unknown": "Tiada tool had cas yang diketahui untuk jenama ini. Semak app PC pengeluar atau halaman kuasa/bateri dalam BIOS. Windows sendiri tiada tetapan had cas.",
        "bypass_note": "Bypass sebenar (bateri diasingkan sepenuhnya dari laluan kuasa) jarang ada, kebanyakannya pada sesetengah laptop gaming, dan battmon tidak boleh mengesannya. Kalau tool pengeluar ada pilihan 'bypass', itulah dia.",
        "guide": "Tempat untuk cari: ",
        "tool_found": "Tool pengeluar dijumpai pada PC ini: {v}",
        "tool_missing": "Tool pengeluar tidak dijumpai pada PC ini (dicari: {v}).",
        "obs_none": "Data belum cukup. Biarkan battmon berjalan semasa dipalam.",
        "obs_range": "Julat log: {a} hingga {b}. Paling rendah {lo}%, paling tinggi {hi}%.",
        "obs_hold": "Semasa dipalam, ia kekal pada {p}% ({n} sampel). Nampak seperti cutoff cas.",
        "obs_full": "Semasa dipalam, ia kekal pada 100% ({n} sampel). Cas penuh biasa, belum nampak cutoff.",
        "gen": "Dijana {t} oleh battmon v{v}",
        "btn_save": "Simpan laporan", "btn_store": "Cari tool pengeluar", "btn_close": "Tutup",
        "saved": "Laporan disimpan:\n{p}", "save_fail": "Gagal simpan: {err}",
    },
}
cfg = {"lang": "en", "no_tray_install": False}
try:
    with open(CFG_FILE, encoding="utf-8") as f:
        _d = json.load(f)
        if _d.get("lang") in STR:
            cfg["lang"] = _d["lang"]
        cfg["no_tray_install"] = bool(_d.get("no_tray_install", False))
except Exception:
    pass


def save_cfg():
    try:
        with open(CFG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
    except Exception:
        pass


def T(k, **kw):
    s = STR[cfg["lang"]].get(k) or STR["en"][k]
    return s.format(**kw) if kw else s


# ================= VENDOR GUIDE =================
VENDORS = [
    {"id": "dell", "name": "Dell", "re": r"dell", "apps": ["Dell Power Manager", "Dell Optimizer", "Dell Command"], "store": "Dell Power Manager"},
    {"id": "hp", "name": "HP", "re": r"\bhp\b|hewlett", "apps": ["HP Support Assistant", "myHP", "HP Power Manager"], "store": "HP Support Assistant"},
    {"id": "lenovo", "name": "Lenovo", "re": r"lenovo", "apps": ["Lenovo Vantage", "Vantage"], "store": "Lenovo Vantage"},
    {"id": "asus", "name": "ASUS", "re": r"asus", "apps": ["MyASUS"], "store": "MyASUS"},
    {"id": "acer", "name": "Acer", "re": r"acer", "apps": ["Acer Care Center", "Care Center"], "store": "Acer Care Center"},
    {"id": "msi", "name": "MSI", "re": r"micro-star|\bmsi\b", "apps": ["MSI Center", "Dragon Center"], "store": "MSI Center"},
    {"id": "samsung", "name": "Samsung", "re": r"samsung", "apps": ["Samsung Settings", "Samsung"], "store": "Samsung Settings"},
    {"id": "microsoft", "name": "Microsoft Surface", "re": r"microsoft", "apps": ["Surface"], "store": "Surface"},
    {"id": "fujitsu", "name": "Fujitsu", "re": r"fujitsu", "apps": ["Fujitsu"], "store": None},
]
VENDOR_GUIDE = {
    "dell": {
        "en": "Dell Power Manager or Dell Optimizer (battery settings), or the BIOS under Power / Battery (Primarily AC use, Custom). battmon controls this directly.",
        "ms": "Dell Power Manager atau Dell Optimizer (tetapan bateri), atau BIOS di bawah Power / Battery (Primarily AC use, Custom). battmon mengawalnya terus.",
    },
    "hp": {
        "en": "Many Pro and Elite models have Battery Health Manager in the BIOS (restart, press F10, then Advanced > Power Management Options). Some also show it in HP Support Assistant.",
        "ms": "Banyak model Pro dan Elite ada Battery Health Manager dalam BIOS (restart, tekan F10, kemudian Advanced > Power Management Options). Sesetengah juga tunjuk dalam HP Support Assistant.",
    },
    "lenovo": {
        "en": "Lenovo Vantage has Conservation Mode in its power or battery section. Many ThinkPads also have charge thresholds in Vantage or in the BIOS power page.",
        "ms": "Lenovo Vantage ada Conservation Mode dalam bahagian power atau battery. Banyak ThinkPad juga ada had cas dalam Vantage atau halaman power BIOS.",
    },
    "asus": {
        "en": "MyASUS > Device Settings > Battery Care mode (some models call it Battery Health Charging).",
        "ms": "MyASUS > Device Settings > Battery Care mode (sesetengah model namakan Battery Health Charging).",
    },
    "acer": {
        "en": "Acer Care Center has a battery health or charge limit option on many newer models. The exact name depends on the version.",
        "ms": "Acer Care Center ada pilihan kesihatan bateri atau had cas pada banyak model baharu. Nama tepat bergantung pada versi.",
    },
    "msi": {
        "en": "MSI Center has battery options on many models (a battery care or charge limit scenario). The exact name depends on the version.",
        "ms": "MSI Center ada pilihan bateri pada banyak model (senario penjagaan bateri atau had cas). Nama tepat bergantung pada versi.",
    },
    "samsung": {
        "en": "Samsung Settings has a battery protection option on many models. The exact name depends on the version.",
        "ms": "Samsung Settings ada pilihan perlindungan bateri pada banyak model. Nama tepat bergantung pada versi.",
    },
    "microsoft": {
        "en": "On supported Surface models, the Surface app or the UEFI settings have a battery limit option.",
        "ms": "Pada model Surface yang disokong, app Surface atau tetapan UEFI ada pilihan had bateri.",
    },
    "fujitsu": {
        "en": "Some Fujitsu models shipped a Battery Utility with an 80% charge mode, and the BIOS setup may have a battery page. Check Fujitsu's support site for your exact model. Many tablets have neither.",
        "ms": "Sesetengah model Fujitsu ada Battery Utility dengan mod cas 80%, dan BIOS mungkin ada halaman bateri. Semak laman sokongan Fujitsu untuk model tepat anda. Banyak tablet tiada kedua-duanya.",
    },
}


# ===== REPORT BUILDER (pure functions, no UI) =====
def vendor_for(mfr):
    m = (mfr or "").lower()
    for v in VENDORS:
        if re.search(v["re"], m):
            return v
    return None


def parse_battery_xml(path):
    out = []
    root_el = ET.parse(path).getroot()
    for el in root_el.iter():
        if el.tag.split("}")[-1] != "Battery":
            continue
        b = {}
        for c in el:
            tag = c.tag.split("}")[-1]
            if len(c) == 0 and (c.text or "").strip():
                b[tag] = c.text.strip()
        if "DesignCapacity" in b or "Id" in b:
            out.append(b)
    return out


def _num(v):
    try:
        return int(float(v))
    except Exception:
        return None


def wh(v):
    n = _num(v)
    return "-" if n is None else f"{n / 1000:.2f} Wh"


def mask_serial(s):
    s = (s or "").strip()
    if not s:
        return T("nr")
    if len(s) <= 6:
        return "*" * len(s)
    return s[:2] + "*" * (len(s) - 6) + s[-4:]


def verdict(pct):
    if pct >= 80:
        return T("v_good")
    if pct >= 60:
        return T("v_worn")
    return T("v_weak")


def charge_lines(d):
    info, cap = d["info"], d["cap"]
    v = vendor_for(info.get("mfr", ""))
    lines = []
    if v and v["id"] == "dell":
        if cap.get("custom"):
            lines.append(("line", T("charge_dell_ok")))
        elif cap.get("bios"):
            lines.append(("line", T("charge_dell_modes")))
        else:
            lines.append(("line", T("charge_dell_no")))
        if cap.get("pw"):
            lines.append(("line", T("note_pw")))
    elif v:
        lines.append(("line", T("charge_vendor", name=v["name"])))
    else:
        lines.append(("line", T("charge_unknown")))
    if v:
        lines.append(("line", T("guide") + VENDOR_GUIDE[v["id"]][cfg["lang"]]))
        found = sorted({n for n in d.get("startapps", []) for p in v["apps"] if p.lower() in n.lower()})
        if found:
            lines.append(("line", T("tool_found", v=", ".join(found))))
        else:
            lines.append(("line", T("tool_missing", v=", ".join(v["apps"]))))
    lines.append(("line", T("bypass_note")))
    return lines


def observed_lines(h):
    if len(h) < 5:
        return [("line", T("obs_none"))]
    pcts = [x[1] for x in h]
    lines = [("line", T("obs_range", a=h[0][0].strftime("%Y-%m-%d %H:%M"), b=h[-1][0].strftime("%Y-%m-%d %H:%M"),
                        lo=min(pcts), hi=max(pcts)))]
    holds = [x[1] for x in h if x[2] == "hold"]
    if len(holds) >= 5:
        p, n = Counter(holds).most_common(1)[0]
        lines.append(("line", T("obs_full", n=n) if p >= 99 else T("obs_hold", p=p, n=n)))
    return lines


def build_sections(d):
    info = d["info"]
    nr = T("nr")
    yn = lambda x: T("yes") if x else T("no")
    secs = [(T("sec_laptop"), [
        ("kv", T("l_maker"), info.get("mfr") or nr),
        ("kv", T("l_model"), info.get("model") or nr),
        ("kv", T("l_bios"), info.get("bios") or nr),
        ("kv", T("l_biosdate"), info.get("biosdate") or nr),
        ("kv", T("l_admin"), yn(d.get("admin"))),
        ("kv", T("l_tray"), yn(d.get("tray"))),
    ])]
    live = d.get("live", {})
    bats = d.get("batteries") or []
    if not bats:
        bats = [{"DesignCapacity": live.get("design"), "FullChargeCapacity": live.get("full"),
                 "CycleCount": live.get("cycles")}]
    for i, b in enumerate(bats, 1):
        design, full = _num(b.get("DesignCapacity")), _num(b.get("FullChargeCapacity"))
        items = [
            ("kv", T("l_id"), b.get("Id") or nr),
            ("kv", T("l_maker"), b.get("Manufacturer") or nr),
            ("kv", T("l_chem"), b.get("Chemistry") or nr),
            ("kv", T("l_serial"), mask_serial(b.get("SerialNumber"))),
            ("kv", T("l_mfgdate"), b.get("ManufactureDate") or nr),
            ("kv", T("f_design"), wh(design) if design else nr),
            ("kv", T("f_full"), wh(full) if full else nr),
        ]
        if design and full:
            pct = full / design * 100
            items.append(("kv", T("f_health"), f"{pct:.1f} %"))
            items.append(("kv", T("l_verdict"), verdict(pct)))
        else:
            items.append(("kv", T("f_health"), nr))
        items.append(("kv", T("f_cycles"), b.get("CycleCount") or nr))
        if i == 1 and live:
            items.append(("kv", T("l_now"), f"{live.get('pct', '-')}%  ({wh(live.get('rem'))})"))
            if live.get("volt"):
                items.append(("kv", T("f_volt"), f"{live['volt'] / 1000:.2f} V"))
        secs.append((T("l_battery_n", n=i), items))
    secs.append((T("sec_charge"), charge_lines(d)))
    secs.append((T("sec_observed"), observed_lines(d.get("hist", []))))
    secs.append((T("sec_notes"), [
        ("line", T("mfg_note")),
        ("line", T("gen", t=datetime.now().strftime("%Y-%m-%d %H:%M"), v=VERSION)),
    ]))
    return secs


def to_text(secs):
    title = T("rep_title")
    out = [title, "=" * len(title), ""]
    for name, items in secs:
        out += [name, "-" * len(name)]
        for it in items:
            out.append(f"{it[1]}: {it[2]}" if it[0] == "kv" else it[1])
        out.append("")
    return "\n".join(out)


def to_html(secs):
    e = _html.escape
    css = ("body{font-family:Segoe UI,Arial,sans-serif;background:#14161a;color:#e8eaee;max-width:760px;margin:30px auto;padding:0 16px}"
           "h1{font-size:22px}h2{font-size:13px;letter-spacing:.08em;color:#8b93a1;border-bottom:1px solid #2a2f38;padding-bottom:4px;margin-top:26px}"
           "table{border-collapse:collapse;width:100%}td{padding:4px 8px;vertical-align:top;font-size:14px}td.k{color:#8b93a1;width:42%}"
           "p{font-size:14px;line-height:1.5}")
    parts = ["<!doctype html><html><head><meta charset='utf-8'><title>", e(T("rep_title")), "</title><style>", css,
             "</style></head><body><h1>", e(T("rep_title")), "</h1>"]
    for name, items in secs:
        parts += ["<h2>", e(name), "</h2>"]
        kv = [x for x in items if x[0] == "kv"]
        if kv:
            parts.append("<table>")
            for it in kv:
                parts += ["<tr><td class='k'>", e(it[1]), "</td><td>", e(str(it[2])), "</td></tr>"]
            parts.append("</table>")
        for it in items:
            if it[0] == "line":
                parts += ["<p>", e(it[1]), "</p>"]
    parts.append("</body></html>")
    return "".join(parts)
# ===== END REPORT BUILDER =====


# ================= HELPERS =================
def msgbox(text, flags=0x40):
    return ctypes.windll.user32.MessageBoxW(0, text, "battmon by Shakir", flags | 0x40000)


def run_ps(cmd, timeout=40):
    return subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True,
                          text=True, timeout=timeout, stdin=subprocess.DEVNULL,
                          creationflags=0x08000000).stdout.strip()


class SPS(ctypes.Structure):
    _fields_ = [("ac", ctypes.c_ubyte), ("flag", ctypes.c_ubyte),
                ("pct", ctypes.c_ubyte), ("sys", ctypes.c_ubyte),
                ("life", ctypes.c_ulong), ("full", ctypes.c_ulong)]


def power_status():
    s = SPS()
    ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(s))
    return s


# ================= ENVIRONMENT CHECK (1): battery present? =================
_s = power_status()
if (_s.flag & 128) or _s.flag == 255:
    msgbox(T("no_battery"))
    sys.exit()

# ================= ENVIRONMENT CHECK (2): which laptop? =================
INFO = {"mfr": "", "model": ""}
try:
    _o = run_ps("$c=Get-CimInstance Win32_ComputerSystem;$c.Manufacturer+'|'+$c.Model")
    INFO["mfr"], _, INFO["model"] = _o.partition("|")
    INFO["mfr"], INFO["model"] = INFO["mfr"].strip(), INFO["model"].strip()
except Exception:
    pass
IS_DELL = "dell" in INFO["mfr"].lower()

# Admin is only requested on Dell, because only Dell charge control writes to the BIOS
if IS_DELL and not ctypes.windll.shell32.IsUserAnAdmin():
    exe = sys.executable
    if not FROZEN and exe.lower().endswith("python.exe"):
        pw_exe = exe[:-10] + "pythonw.exe"
        if os.path.exists(pw_exe):
            exe = pw_exe
    rc = ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, None if FROZEN else f'"{SELF}"', None, 1)
    if rc > 32:
        sys.exit()
    # UAC declined: continue as monitor only

# ================= SINGLE INSTANCE =================
_MUTEX = ctypes.windll.kernel32.CreateMutexW(None, False, "battmon_by_shakir_mutex")
if ctypes.windll.kernel32.GetLastError() == 183:
    sys.exit()

# ================= ENVIRONMENT CHECK (3): tray support =================
pystray = Image = ImageDraw = ImageFont = None


def load_tray_libs():
    global pystray, Image, ImageDraw, ImageFont
    try:
        import pystray as _p
        from PIL import Image as _I, ImageDraw as _D, ImageFont as _F
        pystray, Image, ImageDraw, ImageFont = _p, _I, _D, _F
        return True
    except ImportError:
        return False


if not load_tray_libs() and not FROZEN and not cfg["no_tray_install"]:
    if msgbox(T("tray_ask"), 0x24) == 6:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "-q",
                            "pystray", "pillow"], capture_output=True, timeout=300,
                           stdin=subprocess.DEVNULL, creationflags=0x08000000)
        except Exception:
            pass
        if not load_tray_libs():
            msgbox(T("tray_fail"), 0x10)
    else:
        cfg["no_tray_install"] = True
        save_cfg()

import tkinter as tk

# ================= ENVIRONMENT CHECK (4): BIOS support =================
CAP = {"bios": False, "custom": False, "pw": None}


def detect_bios():
    if not IS_DELL:
        return
    try:
        cmd = ("$ErrorActionPreference='SilentlyContinue';"
               f"$e=Get-CimInstance -Namespace {BIOS_NS} -ClassName EnumerationAttribute;"
               f"$i=Get-CimInstance -Namespace {BIOS_NS} -ClassName IntegerAttribute;"
               "[pscustomobject]@{mode=[bool]($e|?{$_.AttributeName -eq 'PrimaryBattChargeCfg'});"
               "start=[bool]($i|?{$_.AttributeName -eq 'CustomChargeStart'});"
               "stop=[bool]($i|?{$_.AttributeName -eq 'CustomChargeStop'})}|ConvertTo-Json -Compress")
        d = json.loads(run_ps(cmd))
        CAP["bios"] = bool(d.get("mode"))
        CAP["custom"] = bool(d.get("start")) and bool(d.get("stop"))
    except Exception:
        pass
    if CAP["bios"]:
        try:
            o = run_ps("$ErrorActionPreference='SilentlyContinue';"
                       f"(Get-CimInstance -Namespace {PW_NS} -ClassName PasswordObject|?{{$_.NameId -eq 'Admin'}}).IsPasswordSet").strip().lower()
            CAP["pw"] = {"true": True, "false": False}.get(o)
        except Exception:
            pass


detect_bios()


def note():
    if CAP["bios"]:
        return ""
    if not IS_DELL:
        return T("note_other", brand=INFO["mfr"] or "non-Dell")
    return T("note_nobios")


# ================= DATA =================
BG, FG, DIM = "#14161a", "#ffffff", "#8b93a1"
GREEN, YELLOW, RED = "#3ddc84", "#ffc447", "#ff6b6b"
hist = deque(maxlen=2880)
wmi = {}
LEGACY = {"Tengah cas": "charging", "Cas perlahan": "slow", "Guna battery": "batt",
          "Bypass / hold (AC je)": "hold", "AC, tak cas (hold)": "hold"}


def norm_state(s):
    return s if s in ("batt", "charging", "slow", "hold") else LEGACY.get(s, "hold")


def read():
    s = power_status()
    if s.ac != 1:
        state = "batt"
    elif s.flag & 8:
        state = "charging"
    else:
        state = "hold"
    return s.pct, state, s.life


PS = ("$ErrorActionPreference='SilentlyContinue';"
      "$d=Get-CimInstance -Namespace root\\wmi -ClassName BatteryStatus|select -first 1;"
      "$f=Get-CimInstance -Namespace root\\wmi -ClassName BatteryFullChargedCapacity|select -first 1;"
      "$s=Get-CimInstance -Namespace root\\wmi -ClassName BatteryStaticData|select -first 1;"
      "$c=Get-CimInstance -Namespace root\\wmi -ClassName BatteryCycleCount|select -first 1;"
      "[pscustomobject]@{rem=$d.RemainingCapacity;volt=$d.Voltage;chg=$d.ChargeRate;"
      "dis=$d.DischargeRate;full=$f.FullChargedCapacity;design=$s.DesignedCapacity;"
      "cycles=$c.CycleCount}|ConvertTo-Json -Compress")


def wmi_worker():
    while True:
        try:
            wmi.update(json.loads(run_ps(PS, 20)))
        except Exception:
            pass
        time.sleep(10)


threading.Thread(target=wmi_worker, daemon=True).start()


def load_hist():
    try:
        with open(LOG) as f:
            for r in list(csv.DictReader(f))[-1440:]:
                hist.append((datetime.strptime(r["time"], "%Y-%m-%d %H:%M:%S"), int(r["percent"]), norm_state(r["state"])))
    except Exception:
        pass


# ================= WINDOW =================
W = 300
bios = {"mode": "?", "start": None, "stop": None}
cells = {}
field_lbls = {}
mode_btns = {}
state_open = {"v": True}
drag = {"x": 0, "y": 0}
pos = {"full": None}
upd = {"tag": None, "url": None, "shown": False}
rep = {"win": None, "text": None, "sections": None, "store": None, "row": None}

root = tk.Tk()
root.title("battmon by Shakir")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.96)
root.configure(bg=BG, highlightbackground="#2a2f38", highlightthickness=1)
root.geometry("+60+60")


def work_area():
    r = ctypes.wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(48, 0, ctypes.byref(r), 0)
    return r.left, r.top, r.right, r.bottom


def virtual_screen():
    g = ctypes.windll.user32.GetSystemMetrics
    x, y, w, h = g(76), g(77), g(78), g(79)
    return x, y, x + w, y + h


def clamp(snap_bottom=False):
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x, y = root.winfo_x(), root.winfo_y()
    vl, vt, vr, vb = virtual_screen()
    wl, wt, wr, wb = work_area()
    bottom = wb if wl <= x + w // 2 < wr else vb
    if snap_bottom:
        y = bottom - h - 8
    x = min(max(x, vl), vr - w)
    y = min(max(y, vt), bottom - h)
    root.geometry(f"+{x}+{y}")


def d_start(e):
    drag["x"], drag["y"] = e.x, e.y


def d_move(e):
    root.geometry(f"+{e.x_root - drag['x']}+{e.y_root - drag['y']}")


def d_end(e):
    clamp()


def mk_drag(w):
    w.bind("<Button-1>", d_start)
    w.bind("<B1-Motion>", d_move)
    w.bind("<ButtonRelease-1>", d_end)


def toggle_body(e=None):
    if state_open["v"]:
        pos["full"] = (root.winfo_x(), root.winfo_y())
        body.pack_forget()
        state_lbl.pack_forget()
        bar.pack_forget()
        title.config(text="")
        pct_lbl.config(font=("Segoe UI", 28, "bold"))
        mb.config(text="+")
        state_open["v"] = False
        clamp(snap_bottom=True)
    else:
        pct_lbl.config(font=("Segoe UI", 44, "bold"))
        state_lbl.pack()
        bar.pack(pady=(8, 8), padx=14)
        body.pack(fill="x", padx=14, pady=(0, 12))
        title.config(text="battmon  ·  by Shakir")
        mb.config(text="–")
        state_open["v"] = True
        if pos["full"]:
            root.geometry(f"+{root.winfo_x()}+{pos['full'][1]}")
        clamp()


# ================= BIOS =================
def read_bios():
    cmd = ("$ErrorActionPreference='SilentlyContinue';"
           f"$m=(Get-CimInstance -Namespace {BIOS_NS} -ClassName EnumerationAttribute|?{{$_.AttributeName -eq 'PrimaryBattChargeCfg'}}).CurrentValue;"
           f"$s=(Get-CimInstance -Namespace {BIOS_NS} -ClassName IntegerAttribute|?{{$_.AttributeName -eq 'CustomChargeStart'}}).CurrentValue;"
           f"$e=(Get-CimInstance -Namespace {BIOS_NS} -ClassName IntegerAttribute|?{{$_.AttributeName -eq 'CustomChargeStop'}}).CurrentValue;"
           "[pscustomobject]@{mode=$m;start=$s;stop=$e}|ConvertTo-Json -Compress")
    d = json.loads(run_ps(cmd))
    bios["mode"] = d.get("mode") or "?"
    bios["start"] = d.get("start")
    bios["stop"] = d.get("stop")


def set_bios(items):
    cmd = ("$ErrorActionPreference='SilentlyContinue';"
           f"$b=Get-WmiObject -Namespace {BIOS_NS} -Class BIOSAttributeInterface;")
    for n, v in items:
        cmd += f"$r=$b.SetAttribute(0,0,0,'{n}','{v}');Write-Output \"{n}=$($r.Status)\";"
    return run_ps(cmd)


busy = {"v": False}


def apply_async(items, want):
    if busy["v"]:
        msg_lbl.config(text=T("wait"), fg=YELLOW)
        return
    busy["v"] = True
    msg_lbl.config(text=T("applying"), fg=DIM)

    def work():
        try:
            out = set_bios(items)
            read_bios()
            ok = bios["mode"] == want[0]
            if ok and len(want) == 3:
                ok = str(bios["start"]) == str(want[1]) and str(bios["stop"]) == str(want[2])
            if ok:
                txt, col = T("ok"), GREEN
            else:
                txt = T("fail", mode=bios["mode"], start=bios["start"], stop=bios["stop"],
                        out=out.replace(chr(10), " ")) + T("fail_hint")
                col = RED
        except Exception as ex:
            txt, col = f"Error: {ex}", RED
        busy["v"] = False
        root.after(0, lambda: (msg_lbl.config(text=txt, fg=col), refresh_now()))
    threading.Thread(target=work, daemon=True).start()


def bios_refresh():
    if not CAP["bios"]:
        return

    def work():
        try:
            read_bios()
        except Exception:
            pass
    threading.Thread(target=work, daemon=True).start()


def apply_custom():
    try:
        b = int(v_stop.get())
    except ValueError:
        msg_lbl.config(text=T("num_err"), fg=RED)
        return
    a = max(b - 5, 0)
    apply_async([("PrimaryBattChargeCfg", "Custom"), ("CustomChargeStop", b),
                 ("CustomChargeStart", a), ("CustomChargeStop", b)], ("Custom", a, b))


def pick(key):
    if key == "Custom":
        apply_custom()
    else:
        apply_async([("PrimaryBattChargeCfg", key)], (key,))


# ================= UPDATE CHECKER =================
def vtuple(s):
    return tuple(int(x) for x in re.findall(r"\d+", s)[:3])


def check_update():
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases/latest",
                                     headers={"User-Agent": "battmon-updater",
                                              "Accept": "application/vnd.github+json"})
        d = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
        tag = d.get("tag_name", "")
        if vtuple(tag) > vtuple(VERSION):
            upd["tag"] = tag
            upd["url"] = d.get("html_url") or f"https://github.com/{REPO}/releases"
    except Exception:
        pass


def update_loop():
    threading.Thread(target=check_update, daemon=True).start()
    root.after(UPDATE_EVERY * 1000, update_loop)


def do_update(e=None):
    if not upd["tag"]:
        return
    if FROZEN:
        webbrowser.open(upd["url"])
        return
    if msgbox(T("upd_q", cur=VERSION, tag=upd["tag"], repo=REPO), 0x24) != 6:
        return
    try:
        url = f"https://raw.githubusercontent.com/{REPO}/{upd['tag']}/battmon.pyw"
        req = urllib.request.Request(url, headers={"User-Agent": "battmon-updater"})
        code = urllib.request.urlopen(req, timeout=20).read()
        compile(code, "battmon.pyw", "exec")
        if b"VERSION" not in code:
            raise ValueError(T("upd_bad"))
        import shutil
        shutil.copy2(SELF, SELF + ".bak")
        with open(SELF + ".new", "wb") as f:
            f.write(code)
        os.replace(SELF + ".new", SELF)
        subprocess.Popen(f'ping -n 3 127.0.0.1 >nul & "{sys.executable}" "{SELF}"',
                         shell=True, creationflags=0x08000000)
        quit_app()
    except Exception as ex:
        msgbox(T("upd_fail", err=ex), 0x10)


# ================= BATTERY REPORT WINDOW =================
def gather():
    d = {"info": dict(INFO), "admin": bool(ctypes.windll.shell32.IsUserAnAdmin()),
         "tray": pystray is not None, "cap": dict(CAP), "batteries": [], "startapps": [],
         "live": {"pct": cur.get("pct"), "rem": wmi.get("rem"), "volt": wmi.get("volt"),
                  "full": wmi.get("full"), "design": wmi.get("design"), "cycles": wmi.get("cycles")},
         "hist": list(hist)}
    try:
        o = json.loads(run_ps("$ErrorActionPreference='SilentlyContinue';$b=Get-CimInstance Win32_BIOS|select -first 1;"
                              "[pscustomobject]@{v=$b.SMBIOSBIOSVersion;d=$(if($b.ReleaseDate){([datetime]$b.ReleaseDate).ToString('yyyy-MM-dd')})}|ConvertTo-Json -Compress"))
        d["info"]["bios"], d["info"]["biosdate"] = o.get("v"), o.get("d")
    except Exception:
        pass
    try:
        path = os.path.join(tempfile.gettempdir(), "battmon_batteryreport.xml")
        if os.path.exists(path):
            os.remove(path)
        subprocess.run(["powercfg", "/batteryreport", "/xml", "/output", path], capture_output=True, timeout=60,
                       stdin=subprocess.DEVNULL, creationflags=0x08000000)
        d["batteries"] = parse_battery_xml(path)
    except Exception:
        pass
    try:
        names = json.loads(run_ps("Get-StartApps | Select-Object -ExpandProperty Name | ConvertTo-Json -Compress"))
        d["startapps"] = [names] if isinstance(names, str) else list(names)
    except Exception:
        pass
    return d


def mkbtn(parent, text, cmd):
    return tk.Button(parent, text=text, command=cmd, bg="#2a2f38", fg=FG, activebackground="#3a4150",
                     activeforeground=FG, relief="flat", bd=0, padx=14, pady=5,
                     font=("Segoe UI", 9, "bold"), cursor="hand2")


def fill_report(d):
    win = rep["win"]
    if win is None or not win.winfo_exists():
        return
    secs = build_sections(d)
    rep["sections"] = secs
    t = rep["text"]
    t.config(state="normal")
    t.delete("1.0", "end")
    t.insert("1.0", to_text(secs))
    t.config(state="disabled")
    v = vendor_for(d["info"].get("mfr", ""))
    if v and v.get("store") and rep["store"] is None:
        rep["store"] = mkbtn(rep["row"], T("btn_store"),
                             lambda q=v["store"]: os.startfile("ms-windows-store://search/?query=" + urllib.parse.quote(q)))
        rep["store"].pack(side="left", padx=(0, 6))


def save_report():
    if not rep["sections"]:
        return
    try:
        from tkinter import filedialog
        stamp = datetime.now().strftime("%Y%m%d-%H%M")
        path = filedialog.asksaveasfilename(parent=rep["win"], defaultextension=".html",
                                            initialfile=f"battmon-report-{stamp}.html",
                                            filetypes=[("HTML", "*.html"), ("Text", "*.txt")])
        if not path:
            return
        content = to_html(rep["sections"]) if path.lower().endswith(".html") else to_text(rep["sections"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        msgbox(T("saved", p=path))
    except Exception as ex:
        msgbox(T("save_fail", err=ex), 0x10)


def open_report(e=None):
    if rep["win"] is not None and rep["win"].winfo_exists():
        rep["win"].lift()
        return
    win = tk.Toplevel(root)
    win.title(T("rep_win_title"))
    win.configure(bg=BG)
    win.attributes("-topmost", True)
    vl, vt, vr, vb = virtual_screen()
    x = root.winfo_x() + root.winfo_width() + 10
    if x + 600 > vr:
        x = max(root.winfo_x() - 610, vl)
    win.geometry(f"+{x}+{max(root.winfo_y(), vt)}")
    txt = tk.Text(win, width=72, height=32, bg="#0d0f12", fg=FG, font=("Consolas", 9), wrap="word",
                  relief="flat", padx=10, pady=8)
    txt.pack(fill="both", expand=True, padx=10, pady=(10, 6))
    txt.insert("1.0", T("loading"))
    txt.config(state="disabled")
    row = tk.Frame(win, bg=BG)
    row.pack(fill="x", padx=10, pady=(0, 10))
    mkbtn(row, T("btn_save"), save_report).pack(side="left", padx=(0, 6))
    mkbtn(row, T("btn_close"), win.destroy).pack(side="right")
    rep.update({"win": win, "text": txt, "sections": None, "store": None, "row": row})

    def work():
        d = gather()
        root.after(0, lambda: fill_report(d))
    threading.Thread(target=work, daemon=True).start()


# ================= LAYOUT =================
logo_img = None
if LOGO_B64.strip():
    try:
        logo_img = tk.PhotoImage(data=LOGO_B64.strip())
        if logo_img.height() > 28:
            logo_img = logo_img.subsample(max(logo_img.height() // 22, 1))
    except tk.TclError:
        logo_img = None

top = tk.Frame(root, bg=BG)
top.pack(fill="x")
if logo_img:
    logo_lbl = tk.Label(top, image=logo_img, bg=BG)
    logo_lbl.image = logo_img
else:
    logo_lbl = tk.Label(top, text="⚡", fg=GREEN, bg=BG, font=("Segoe UI", 11))
logo_lbl.pack(side="left", padx=(10, 0))
title = tk.Label(top, text="battmon  ·  by Shakir", fg=DIM, bg=BG, font=("Segoe UI", 9), padx=6, pady=6)
title.pack(side="left")
xb = tk.Label(top, text="✕", fg=DIM, bg=BG, font=("Segoe UI", 10), padx=10, cursor="hand2")
xb.pack(side="right")
xb.bind("<Button-1>", lambda e: hide_tray(e))
mb = tk.Label(top, text="–", fg=DIM, bg=BG, font=("Segoe UI", 10, "bold"), padx=8, cursor="hand2")
mb.pack(side="right")
mb.bind("<Button-1>", toggle_body)
tb = tk.Label(top, text="▾", fg=DIM, bg=BG, font=("Segoe UI", 10), padx=8, cursor="hand2")
tb.pack(side="right")
tb.bind("<Button-1>", lambda e: hide_tray(e))
LANG_TXT = {"en": "EN", "ms": "MY"}
lang_lbl = tk.Label(top, text=LANG_TXT[cfg["lang"]], fg="#6ea8fe", bg=BG, font=("Segoe UI", 9, "bold"), padx=8, cursor="hand2")
lang_lbl.pack(side="right")
lang_lbl.bind("<Button-1>", lambda e: toggle_lang())

pct_lbl = tk.Label(root, text="--%", font=("Segoe UI", 44, "bold"), fg=FG, bg=BG, padx=20)
pct_lbl.pack()
state_lbl = tk.Label(root, text="", fg=DIM, bg=BG, font=("Segoe UI", 11))
state_lbl.pack()
bar = tk.Canvas(root, width=W, height=10, bg=BG, highlightthickness=0)
bar.pack(pady=(8, 8), padx=14)
for w_ in (top, logo_lbl, title, pct_lbl, state_lbl):
    mk_drag(w_)
pct_lbl.bind("<Double-Button-1>", toggle_body)

body = tk.Frame(root, bg=BG)
body.pack(fill="x", padx=14, pady=(0, 12))

FIELDS = ["volt", "rate", "left", "cap", "full", "design", "health", "cycles"]
if CAP["bios"]:
    FIELDS += ["mode", "limit"]
info = tk.Frame(body, bg=BG)
info.pack(fill="x")
for i, k in enumerate(FIELDS):
    c = tk.Frame(info, bg=BG)
    c.grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 22), pady=3)
    fl = tk.Label(c, text=T("f_" + k), fg=DIM, bg=BG, font=("Segoe UI", 8))
    fl.pack(anchor="w")
    field_lbls[k] = fl
    v = tk.Label(c, text="-", fg=FG, bg=BG, font=("Segoe UI", 11, "bold"))
    v.pack(anchor="w")
    cells[k] = v

cv = tk.Canvas(body, width=W, height=130, bg="#0d0f12", highlightthickness=0)
cv.pack(pady=(10, 10))


class Tip:
    def __init__(self, w, key):
        self.w, self.key, self.tw = w, key, None
        w.bind("<Enter>", self.show)
        w.bind("<Leave>", self.hide)

    def show(self, e=None):
        if self.tw:
            return
        self.tw = tk.Toplevel(self.w)
        self.tw.overrideredirect(True)
        self.tw.attributes("-topmost", True)
        self.tw.geometry(f"+{self.w.winfo_rootx()}+{self.w.winfo_rooty() + self.w.winfo_height() + 6}")
        tk.Label(self.tw, text=T(self.key), justify="left", bg="#2a2f38", fg=FG,
                 font=("Segoe UI", 9), padx=8, pady=6, wraplength=260).pack()

    def hide(self, e=None):
        if self.tw:
            self.tw.destroy()
            self.tw = None


v_stop = tk.StringVar(value="80")
limit_lbl = None
charge = tk.Frame(body, bg=BG)
if CAP["bios"]:
    charge.pack(fill="x")
charge_hdr = tk.Label(charge, text=T("charge_mode"), fg=DIM, bg=BG, font=("Segoe UI", 8, "bold"))
charge_hdr.pack(anchor="w")
mrow = tk.Frame(charge, bg=BG)
mrow.pack(fill="x", pady=4)
modes = ["Standard", "PrimAcUse"]
if CAP["custom"]:
    modes.append("Custom")
for key in modes:
    b = mkbtn(mrow, T("btn_" + key), lambda k=key: pick(k))
    b.pack(side="left", padx=(0, 6))
    mode_btns[key] = b
    Tip(b, "tip_" + key)

if CAP["custom"]:
    crow = tk.Frame(charge, bg=BG)
    crow.pack(fill="x", pady=(4, 0))
    limit_lbl = tk.Label(crow, text=T("limit"), fg=DIM, bg=BG, font=("Segoe UI", 9))
    limit_lbl.pack(side="left", padx=(0, 6))
    for lim in ("50", "80", "90"):
        tk.Radiobutton(crow, text=lim + "%", value=lim, variable=v_stop, command=apply_custom,
                       indicatoron=False, bg="#2a2f38", fg=FG, selectcolor="#2f7d52",
                       activebackground="#3a4150", activeforeground=FG, relief="flat", bd=0,
                       padx=12, pady=4, font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side="left", padx=(0, 4))

msg_lbl = tk.Label(charge, text=T("note_pw") if CAP["pw"] else "", fg=YELLOW, bg=BG,
                   font=("Segoe UI", 8), wraplength=W, justify="left")
msg_lbl.pack(anchor="w", pady=(6, 0))
explain_lbl = tk.Label(body, text="", fg=FG, bg="#1a1d23", font=("Segoe UI", 9), wraplength=W - 16, justify="left", padx=8, pady=6)
explain_lbl.pack(fill="x", pady=(8, 0))

foot = tk.Frame(body, bg=BG)
foot.pack(fill="x", pady=(10, 0))


def link(text, url=None, cmd=None):
    l = tk.Label(foot, text=text, fg="#6ea8fe", bg=BG, font=("Segoe UI", 8, "underline"), cursor="hand2")
    l.bind("<Button-1>", (lambda e: webbrowser.open(url)) if url else (lambda e: cmd()))
    return l


def dot():
    tk.Label(foot, text="·", fg=DIM, bg=BG, font=("Segoe UI", 8)).pack(side="left", padx=4)


link("LinkedIn", url=LINKEDIN).pack(side="left")
dot()
link("GitHub", url=GITHUB).pack(side="left")
dot()
check_lbl = link(T("check"), cmd=open_report)
check_lbl.pack(side="left")
tk.Label(foot, text=f"v{VERSION}", fg=DIM, bg=BG, font=("Segoe UI", 8)).pack(side="right")
upd_lbl = tk.Label(body, text="", fg="#000000", bg=GREEN, font=("Segoe UI", 9, "bold"), cursor="hand2", padx=8, pady=4, wraplength=W - 16)
upd_lbl.bind("<Button-1>", do_update)


# ================= UPDATE UI =================
def fmt(v, div, unit, nd=1):
    return "-" if v is None else f"{v / div:.{nd}f} {unit}"


def update_details(pct, state, life):
    w = wmi
    rate = w.get("chg") or w.get("dis")
    full, design = w.get("full"), w.get("design")
    health = f"{full / design * 100:.1f} %" if full and design else "-"
    left = "-" if life in (0xFFFFFFFF, None) else T("h_min", h=life // 3600, m=(life % 3600) // 60)
    names = {"Standard": T("btn_Standard"), "PrimAcUse": "Hold AC", "Custom": "Custom",
             "Adaptive": "Adaptive", "Express": "Express"}
    vals = {
        "volt": fmt(w.get("volt"), 1000, "V", 2),
        "rate": fmt(rate, 1000, "W"),
        "left": left,
        "cap": fmt(w.get("rem"), 1000, "Wh", 2),
        "full": fmt(full, 1000, "Wh", 2),
        "design": fmt(design, 1000, "Wh", 2),
        "health": health,
        "cycles": "-" if w.get("cycles") is None else str(w.get("cycles")),
        "mode": names.get(bios["mode"], bios["mode"]),
        "limit": f"{bios['stop']}% / {bios['start']}%" if bios["mode"] == "Custom" and bios["stop"] is not None else "-",
    }
    for k, v in vals.items():
        if k in cells:
            cells[k].config(text=v)
    for key, b in mode_btns.items():
        on = bios["mode"] == key
        b.config(bg=GREEN if on else "#2a2f38", fg="#000000" if on else FG)
    explain_lbl.config(text=explain(pct, state))
    if not busy["v"] and bios["mode"] == "Custom" and bios["stop"] is not None:
        v_stop.set(str(int(bios["stop"])))


cur = {"pct": 0, "col": FG, "state": "", "life": None}
phase = {"v": 0}


def explain(pct, state):
    if not CAP["bios"]:
        return note()
    m, a, b = bios["mode"], bios["start"], bios["stop"]
    if m == "Standard":
        return T("ex_full")
    if m == "PrimAcUse":
        return T("ex_hold")
    if m == "Custom" and a is not None and b is not None:
        a, b = int(a), int(b)
        if state == "batt":
            return T("ex_batt", b=b)
        if pct >= a:
            return T("ex_nocharge", b=b, pct=pct)
        return T("ex_charge", a=a, b=b)
    return ""


def draw_bar(pct, col):
    bar.delete("all")
    bar.create_rectangle(0, 0, W, 10, fill="#262a32", outline="")
    custom = bios["mode"] == "Custom" and bios["start"] is not None and bios["stop"] is not None
    if custom:
        bar.create_rectangle(W * int(bios["start"]) / 100, 0, W * int(bios["stop"]) / 100, 10, fill="#323a48", outline="")
    fw = W * pct / 100
    bar.create_rectangle(0, 0, fw, 10, fill=col, outline="")
    st, p = cur["state"], phase["v"]
    if st in ("charging", "slow"):
        x1 = max((p * 5) % (fw + 40) - 40, 0)
        x2 = min((p * 5) % (fw + 40), fw)
        if x2 > x1:
            bar.create_rectangle(x1, 0, x2, 10, fill="#ffffff", stipple="gray50", outline="")
    elif st == "hold":
        r = 2 + abs((p % 20) - 10) * 0.3
        bar.create_oval(fw - r, 5 - r, fw + r, 5 + r, outline=FG)
    if custom:
        for v in (bios["start"], bios["stop"]):
            x = W * int(v) / 100
            bar.create_line(x, 0, x, 10, fill=FG, width=2)


def refresh_now():
    update_details(cur["pct"], cur["state"], cur.get("life"))
    draw_bar(cur["pct"], cur["col"])


def anim():
    phase["v"] += 1
    if state_open["v"]:
        draw_bar(cur["pct"], cur["col"])
    root.after(100, anim)


def draw_graph():
    cv.delete("all")
    H, L, B, T_ = 130, 26, 16, 8
    for p in (0, 50, 100):
        y = T_ + (H - T_ - B) * (1 - p / 100)
        cv.create_line(L, y, W - 6, y, fill="#23272e")
        cv.create_text(L - 4, y, text=str(p), fill=DIM, font=("Segoe UI", 7), anchor="e")
    pts = list(hist)
    if len(pts) < 2:
        return
    t0, t1 = pts[0][0].timestamp(), pts[-1][0].timestamp()
    span = max(t1 - t0, 1)

    def xy(r):
        return (L + (W - 6 - L) * (r[0].timestamp() - t0) / span, T_ + (H - T_ - B) * (1 - r[1] / 100))
    for a, b in zip(pts, pts[1:]):
        col = {"charging": GREEN, "slow": GREEN, "batt": RED}.get(b[2], YELLOW)
        x1, y1 = xy(a)
        x2, y2 = xy(b)
        cv.create_line(x1, y1, x2, y2, fill=col, width=2)
    cv.create_text(L, H - 5, text=pts[0][0].strftime("%d/%m %H:%M"), fill=DIM, font=("Segoe UI", 7), anchor="w")
    cv.create_text(W - 6, H - 5, text=pts[-1][0].strftime("%d/%m %H:%M"), fill=DIM, font=("Segoe UI", 7), anchor="e")


# ================= TRAY =================
tray = {"icon": None, "cmd": None, "last": None}


def make_icon(pct, col):
    img = Image.new("RGBA", (64, 64), (20, 22, 26, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 63, 63), outline=col, width=4)
    try:
        d.text((32, 34), str(pct), fill=col, font=ImageFont.load_default(size=38), anchor="mm")
    except Exception:
        d.text((16, 26), str(pct), fill=col)
    return img


def tray_cmd(c):
    def f(icon, item):
        tray["cmd"] = c
    return f


def build_menu():
    return pystray.Menu(pystray.MenuItem(T("tray_open"), tray_cmd("show"), default=True),
                        pystray.MenuItem(T("tray_exit"), tray_cmd("exit")))


def start_tray():
    if pystray is None:
        return
    tray["icon"] = pystray.Icon("battmon", make_icon(0, FG), "battmon", build_menu())
    tray["icon"].run_detached()


def update_tray(pct, col):
    ic = tray["icon"]
    if ic is None or tray["last"] == (pct, col):
        return
    tray["last"] = (pct, col)
    try:
        ic.icon = make_icon(pct, col)
        ic.title = f"battmon {pct}%"
    except Exception:
        pass


def hide_tray(e=None):
    if tray["icon"]:
        root.withdraw()
    elif msgbox(T("close_quit"), 0x24) == 6:
        root.destroy()


def quit_app():
    try:
        if tray["icon"]:
            tray["icon"].stop()
    except Exception:
        pass
    root.destroy()


def poll_cmd():
    c = tray["cmd"]
    tray["cmd"] = None
    if c == "show":
        root.deiconify()
        root.attributes("-topmost", True)
        clamp()
    elif c == "exit":
        quit_app()
        return
    root.after(300, poll_cmd)


# ================= LANGUAGE SWITCH =================
def apply_lang():
    lang_lbl.config(text=LANG_TXT[cfg["lang"]])
    for k, l in field_lbls.items():
        l.config(text=T("f_" + k))
    charge_hdr.config(text=T("charge_mode"))
    if limit_lbl:
        limit_lbl.config(text=T("limit"))
    for key, b in mode_btns.items():
        b.config(text=T("btn_" + key))
    check_lbl.config(text=T("check"))
    msg_lbl.config(text=T("note_pw") if CAP["pw"] else "", fg=YELLOW)
    if tray["icon"]:
        try:
            tray["icon"].menu = build_menu()
            tray["icon"].update_menu()
        except Exception:
            pass
    update_ui()


def toggle_lang():
    cfg["lang"] = "ms" if cfg["lang"] == "en" else "en"
    save_cfg()
    apply_lang()


# ================= LOOP =================
last_log = 0
last_state = None
count = 0
if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        csv.writer(f).writerow(["time", "percent", "state"])
load_hist()
bios_refresh()
start_tray()
root.after(300, poll_cmd)
root.after(5000, update_loop)
anim()


def update_ui():
    global last_log, last_state, count
    pct, state, life = read()
    if state != "batt" and wmi.get("chg") is not None:
        cw = (wmi.get("chg") or 0) / 1000
        state = "charging" if cw >= 5 else ("slow" if cw > 0 else "hold")
    if state in ("charging", "slow"):
        col = GREEN
    elif state == "batt":
        col = RED if pct <= 20 else FG
    else:
        col = YELLOW
    pct_lbl.config(text=f"{pct}%", fg=col)
    state_lbl.config(text=T("st_" + state), fg=col)
    now = time.time()
    if now - last_log >= LOG_EVERY or state != last_state:
        with open(LOG, "a", newline="") as f:
            csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pct, state])
        hist.append((datetime.now(), pct, state))
        last_log = now
        last_state = state
    count += 1
    if count % 30 == 0:
        bios_refresh()
    if upd["tag"]:
        upd_lbl.config(text=T("banner_exe" if FROZEN else "banner", tag=upd["tag"]))
        if not upd["shown"]:
            upd_lbl.pack(fill="x", pady=(8, 0), before=foot)
            upd["shown"] = True
    cur["pct"], cur["col"], cur["state"], cur["life"] = pct, col, state, life
    update_details(pct, state, life)
    update_tray(pct, col)
    draw_graph()


def tick():
    update_ui()
    root.after(INTERVAL * 1000, tick)


tick()
clamp()
root.mainloop()

