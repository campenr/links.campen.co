$(document).ready(function(){

    // Instantiate clipboard button event listeners
    new Clipboard('.copy-button');

    // Iterate over table rows amending certain cells as necessary
    $('.link-table-body').children().each(function(tableRowIndex, tableRow){
        // Create href attribute with valid URL endpoint for 'a' element
        var linkToken = $(tableRow).attr("id");
        var shortLinkElem = tableRow.getElementsByClassName("link-token")[0].getElementsByTagName("a");
        var shortLink = location.host + "/" + linkToken;
        $(shortLinkElem).attr("href", (location.protocol + "//" + shortLink));
        $(shortLinkElem).text(shortLink);

        // Create target for copy button
        var copyButton = tableRow.getElementsByClassName("copy-button")[0];
        var target = $(shortLinkElem).attr("href");
        $(copyButton).attr("data-clipboard-text", target);

    });    // Close iterate over table rows

});    // Close document.ready