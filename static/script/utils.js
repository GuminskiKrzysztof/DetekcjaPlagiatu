export function toggleVisibility(element) {
    if (element.style.display === "none") {
        element.style.display = "";
    } else {
        element.style.display = "none";
    }
}