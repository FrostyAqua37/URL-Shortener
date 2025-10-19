function clipboard() {
    let link = document.getElementById("shortenedURL");
    link.select();
    link.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(link.value);
    alert('Copied to Clipboard');
}   