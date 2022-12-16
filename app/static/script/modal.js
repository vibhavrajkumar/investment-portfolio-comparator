$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    // this is how we add a portfolio
    $('#portfolio-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const portfolioID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (portfolioID === 'New Investment') {
            modal.find('.modal-title').text(portfolioID)
            $('#portfolio-form-display').removeAttr('portfolioID')
        } else {
            modal.find('.modal-title').text('Edit Investment ' + portfolioID)
            $('#portfolio-form-display').attr('portfolioID', portfolioID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })
    


    $('#submit-portfolio').click(function () {
        const tID = $('#portfolio-form-display').attr('portfolioID');
        console.log($('#portfolio-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description': $('#portfolio-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    // $('#search-button').click(function () {

    //     var input = document.getElementById('search-bar').value
    //     console.log(input)
    //     $.ajax({
    //         type: 'GET',
    //         url: '/filter/' + input,
    //         contentType: 'application/json;charset=UTF-8',
            
    //         success: function (res) {
    //             console.log("AWW YEAH WE PASSED")
    //             location.replace(link)
    //         },
    //         error: function () {
    //             console.log('Error');
    //         }
    //     });
    // });
});