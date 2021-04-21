$(document).ready(function () {
    $('#add').hide()
    $('#notAuth').hide()
    $('#yesAuth').hide()
    $('.add_clear').hide()
    $('#description').hide()
    $('#menu-phone').hide()

    $('.info-eyes').hide()

    $('.eyes').hover(function (){
        $(this).prev().show(500)
            },function (){
        $(this).prev().stop().hide(200)
        }
        ) // end hover
    $('.fa-trash').stop().hover(function (){
        $('#description').show(300)


    },function (){
        $('#description').hide(300)
    }).stop() // end hover
    $('.clear').click(function () {


        $(this).parent().parent().hide(2000)

        var show_pk = $(this).parent().prev().prev().text()
        // var user_pk = window.document.URL.split('/')[4]
        $.getJSON('delete/', {'show_pk':show_pk}, function (data){
            if (data.data == 'ok'){
                $('.add_clear').show(200).delay(1000).hide(500);

            }
        })


    }) // end click


    $('#Subscribe').click(function () {
        $('#add').toggle(200)
        var pk = window.document.URL.split('/')[4];
        $.getJSON('subscribe_ajax/', {'value': pk}, function (data) {
            if (data.key) {
                var name = data.show_rus;
                var name2 = data.show_en;
                if (name) {
                    $('#yesAuth').text(`шоу ${name} добавлено в колекцию`).show(500).delay(3000).hide(500)

                } else {
                    $('#yesAuth').text(`шоу ${name2} добавлено в колекцию`).show(500).delay(3000).hide(500)
                }


            } else {
                $('#notAuth').show(500).delay(3000).hide(500);

            }


        })// end ajax


        return false

    });// end click

    $('#Subscribe').hover(function () {

            $('#add').show(500)


        },
        function () {
            $('#add').hide(500)
        }
    )// end hover


    $('#ButtonSearch').click(function () {
        var $button = $('#ButtonSearch');
        var $search = $('#search');


        $search.animate({
                width: '100%',

            },
            1500,
            function () {
                $search.removeClass('jsInput');
                $button.removeClass('jsButton');
                $button.addClass('button');
                $search.addClass('input');


            }
        );// end animate


        return false
    });

    $('.show-raiting').hover(function () {

        $(this).stop().animate({
                opacity: 1,
            },
            300
        );// end animate
        $('.show-raiting').show(1000);

    });// end hover

    $('.show-raiting').mouseout(function () {

        $(this).stop().animate({
                opacity: 0,

            },
            100
        )

    }); // end mouseoute
    function checkVal($this) {
        let val = $this.val()
        if (val.length > 1) {
            $.getJSON("search/", {'value': val},
                function (data, textStatus, jqXHR) {
                    if (data.length == 0) {
                        $('.complication').remove();

                    }
                    let html = '';
                    for (let i = 0; i < data.length; i++) {
                        let new_html = `<a href="${data[i][4]}" class='url-search-show'><div class="search-show">
                        <img src="${data[i][3]}">
                        <div class="name-rus-en">
                          <p class="date">${data[i][2]}</p>
                          <p class="ru">${data[i][1]}</p>
                          <p class="en">${data[i][0]}</p>
                        </div>
                      </div></a>`;
                        html += new_html

                    }
                    $('.compilation').html(html);


                }
            );
        } else {
            $('.complication').remove()

        }


    }



   

    var keyupCount = 0;
    $('#search').keyup(function () {
        $this = $(this)
        let time = setTimeout(checkVal, 0, $this);


    });// end focus
    $('#search').blur(function () {
        $('.complication').remove();

    });// end blur


    // -------------------------------------------------------------------------------------------------------- //




    function checkValPhone($this) {
        let val = $this.val()
        if (val.length > 1) {
            $.getJSON("search/", {'value': val},
                function (data, textStatus, jqXHR) {
                    if (data.length == 0) {
                        $('.complication-2').remove();

                    }
                    let html = '';
                    for (let i = 0; i < data.length; i++) {
                        let new_html = `<a href="${data[i][4]}" class='url-search-show'><div class="search-show">
                        <img src="${data[i][3]}">
                        <div class="name-rus-en">
                          <p class="date">${data[i][2]}</p>
                          <p class="ru">${data[i][1]}</p>
                          <p class="en">${data[i][0]}</p>
                        </div>
                      </div></a>`;
                        html += new_html

                    }
                    $('.compilation-2').html(html);


                }
            );
        } else {
            $('.complication-2').remove()

        }


    }

    var keyupCount = 0;
    $('#search-phone').keyup(function () {
        $this = $(this)
        let time = setTimeout(checkValPhone, 0, $this);


    });// end focus
    $('#search-phone').blur(function () {
        $('.complication-2').remove();

    });// end blur

    
    $('#menu-bars').click(function(){
        $('#menu-phone').fadeToggle(500)

    }); //end click

}); // end ready