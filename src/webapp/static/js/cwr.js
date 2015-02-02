/**
 * Created by Borja on 7/24/2014.
 */

function togglePanels(panelType) {
    if (!panelType.checked) {
        $("." + panelType.id).hide();
        panelType.checked = false
    } else {
        $("." + panelType.id).show();
        panelType.checked = true
    }
}

function loadQuickLinks(textinput) {
    $("#trans-quick-search").attr("href", "#trans_" + $(textinput).val());
    $("#rec-quick-search").attr("href", "#rec_" + $(textinput).val());
}