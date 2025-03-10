document.addEventListener("DOMContentLoaded", function () {
    let cooldownMessage = document.getElementById("cooldown-message");
    if (cooldownMessage) {
        setTimeout(() => {
            cooldownMessage.style.display = "none";
        }, 5000);
    }
});
