/**
 * Created by Borja on 7/24/2014.
 */
function togglePanels(panelType) {
    if (!panelType.checked) {
        $("." + panelType.id).hide()
        panelType.checked = false
    } else {
        $("." + panelType.id).show()
        panelType.checked = true
    }
}