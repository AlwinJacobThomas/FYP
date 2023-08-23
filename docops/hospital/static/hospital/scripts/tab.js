document.addEventListener("DOMContentLoaded", function () {
    var tabLabels = document.querySelectorAll(".tab-controllers label");
    var tabPanels = document.querySelectorAll(".tab-panel");

    function switchTab(event) {
        var targetTabId = this.getAttribute("for");
        tabPanels.forEach(function (panel) {
            panel.style.display = panel.id === targetTabId ? "flex" : "none";
        });
        tabLabels.forEach(function (label) {
            label.classList.toggle("active", label.getAttribute("for") === targetTabId);
        });
    }

    tabLabels.forEach(function (label) {
        label.addEventListener("click", switchTab);
    });

    // Set the initial active tab
    var initialActiveTabId = tabLabels[0].getAttribute("for");
    document.getElementById(initialActiveTabId).style.display = "flex";
    tabLabels[0].classList.add("active");
});
