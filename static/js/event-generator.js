var go = function () {
    var isInstalled = document.documentElement.getAttribute('extension-installed');
    if (isInstalled=="true") {
        var event = document.createEvent('Event');
        event.initEvent('invokeVkEvent');
        document.dispatchEvent(event);
    }
    else {
        //code to change background image
        //document.getElementById("masthead").style.backgroundImage = 'url(buttons/' + 'd' + '.png)';        
        $("#myModal").modal();
    }
}