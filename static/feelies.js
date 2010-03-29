
$(function() {
    var make_link = function(title) {
        var href = window.location.href;
        var path_parts = window.location.pathname.split('/').slice(1);
        if (title !== 'manifesto') {
            if (path_parts.length > 2) {
                return window.location.protocol + '//' +
                    window.location.host + '/' + path_parts[0] + '/' +
                    path_parts[1] + '/' + encodeURIComponent(title);
            } else {
                return href + "/" + encodeURIComponent(title);
            }
        } else {
            if (path_parts.lenght < 3) {
                return href;
            } else {
                return window.location.protocol + '//' + 
                    window.location.host + '/' + path_parts[0] + '/' +
                    path_parts[1];
            }
        }
    };

    var recent_changes = function() {
        var bag = new TiddlyWeb.Bag(dictionary_bag, window.location.protocol +
                '//' + window.location.host);
        var details = $("#details");
        bag.tiddlers().get(
            function(data, status, xhr) {
                $.each(data, function(index, tiddler) {
                    details.append('<li><a href="' + make_link(tiddler.title)
                        + '">' + tiddler.title + '</a></li>\n');
                    });
            },
            function(data, start, xhr) {
                details.append('<li>' + status + '</li>');
            },
            'sort=-modified;limit=10'
        );
    };

    $("#cancel").hide();
    recent_changes();

    $("#contextify").click( function() {
        var selection = window.getSelection();
        selection = jQuery.trim(selection.toString().toLowerCase().replace(/\s+/, ' '));
        if (selection) {
            window.location.href = make_link(selection);
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
        
        var cancel_edit = function(old_content) {
            editing = false;
            $("#cancel").hide();
            c.get(0).contentEditable = false;
            c.html(old_content);
            c.css({background:'white'});
            $("#pontificate").css({background:'white'});
        }

        var toggle_edit = function() {
            switch(editing) {
                case true:
                    c.get(0).contentEditable = false;
                    save_it_up(c);
                    break;
                case false:
                    var saved_html = c.html();
                    c.get(0).contentEditable = true;
                    $("#cancel").show('fast').click( function() {
                        cancel_edit(saved_html);
                    });
                    c.css({background:'lightyellow'});
                    $("#pontificate").css({background:'lightyellow'});
                    editing = true;
                    break;
                }
        }

        var save_it_up = function(content) {
            c.fadeOut('slow');
            $("#cancel").hide('slow');
            target_tiddler = new TiddlyWeb.Tiddler(tiddler);
            target_tiddler.bag = new TiddlyWeb.Bag(this_bag, window.location.protocol +
                    '//' + window.location.host);
            content.html(content.html().replace(/<br>/g, "\n").
                    replace(/<div>/g, "\n").
                    replace(/<\/div>/g, ""));
            target_tiddler.text = content.text().replace(/\n{3,}/g, "\n\n");
            target_tiddler.put(
                    function(data, status ,xhr) {
                        window.location.href = make_link(tiddler);
                    },
                    function(data, status, xhr) {
                        c.fadeIn('fast');
                    });
        }
    }
});
