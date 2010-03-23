
$(function() {
    $("#contextify").click( function() {
        var selection = window.getSelection();
        selection = jQuery.trim(selection.toString().toLowerCase().replace(/\s+/, ' '));
        if (selection) {
            var href = window.location.href;
            var path_parts = window.location.pathname.split('/').slice(1);
            if (path_parts.length > 2) {
                window.location.href = window.location.protocol + '//' +
                    window.location.host + '/' + path_parts[0] + '/' +
                    path_parts[1] + '/' + encodeURIComponent(selection);
            } else {
                window.location.href = href + "/" + encodeURIComponent(selection);
            }
        }
    });

    $("#manifest").click( function() {
        var href = window.location.href;
        var path_parts = window.location.pathname.split('/').slice(1);
        window.location.href = window.location.protocol + '//' +
                window.location.host + '/' + path_parts[0];
    });
    
    $(".activate input:not(.grayed)").hover(
        function(){ $(this).css('color', 'red');},
        function(){ $(this).css('color', 'black');}
    );

    $(".activate input:.grayed").hover(
        function(){ $(this).css('color', 'gray');},
        function(){ $(this).css('color', 'black');}
    );

    if (weAuthed) {
        var editing = false;
        var c = $("#content");
        $("#pontificate").click( function() {
                toggle_edit();
        });

        var toggle_edit = function() {
            switch(editing) {
                case true:
                    c.get(0).contentEditable = false;
                    save_it_up(c);
                    break;
                case false:
                    c.get(0).contentEditable = true;
                    c.css({background:'lightyellow'});
                    $("#pontificate").css({background:'lightyellow'});
                    editing = true;
                    break;
                }
        }

        var save_it_up = function(content) {
            c.fadeOut('slow', function() { c.fadeIn('fast');});
            target_tiddler = new TiddlyWeb.Tiddler(tiddler);
            target_tiddler.bag = new TiddlyWeb.Bag(bag, window.location.protocol +
                    '//' + window.location.host);
            target_tiddler.text = content.text();
            target_tiddler.put(
                    function(data, status ,xhr) {
                        c.css({background:'white'});
                        $("#pontificate").css({background:'white'});
                        editing = false;
                    },
                    function(data, status, xhr) {
                        alert('hmmm: ' + status + data);
                    });
        }
    }
});
