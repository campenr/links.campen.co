import 'bootstrap/js/dist/util';
import 'bootstrap/js/dist/alert';
const Clipboard = require('clipboard');
const $ = require('jquery');
require('datatables.net-bs4');

$(document).ready(function(){

    // Instantiate data table contents from ajax call
    var linkTable = $('#link-table').DataTable({
        "autoWidth": false,
        "info": false,
        "lengthChange": false,
        "order": [[ 1, "desc" ]],
        "searching": false,
        "processing": true,
        "serverSide": true,
        columns: [
            {name: 'long_link', data: 'long_link'},
            {name: 'created', data: 'created'},
            {name: 'short_link', data: 'short_link'},
            {name: 'copy', data: 'copy', "orderable": false},
            {name: 'delete', data: 'delete', "orderable": false}
        ],
        ajax: {
            url: 'api/links',
            cache: true,
            data: function(result){
                // format ajax request data
                // only interested in sending what column we're sorting by and what direction

                // get currently sorted column and direction
                var sortedColumnNum = result['order'][0]['column'];
                var sortedColumn = result['columns'][sortedColumnNum]['name'];
                var pageStart = result['start']

                var sortDirection = result['order'][0]['dir'];
                var sortDesc = sortDirection === 'desc';

                return {
                    'column': sortedColumn,
                    'desc': sortDesc,
                    'start': pageStart
                }
            }
        },
        "columnDefs": [
            {
                // create hyperlink for long link
                "targets": 0,
                "data": "long_link",
                "render": function ( data, type, full, meta ) {
                    return '<a href="' + data['url'] + '">' + data['name'] + '</a>';
                }
            },
            {
                // create hyperlink for short link
                "targets": 2,
                "data": "short_link",
                "render": function ( data, type, full, meta ) {
                    var shortLink = location.host + '/' + data;
                    return '<a href="' + data + '">' + shortLink + '</a>';
                }
            },
            {
                // add copy button for this link
                "targets": 3,
                "render": function ( data, type, full, meta ) {
                    return '<button class="btn copy-button" title="copy to clipboard" data-clipboard-text="' + location.protocol + '//' + location.host + '/' + data + '"><i class="fal fa-copy" aria-hidden="true"></i></button>'
                }
            },
            {
                // add delete button for this link
                "targets": 4,
                "render": function ( data, type, full, meta ) {
                    return '<form action="/api/link/delete" method="post" onsubmit="return confirm(\'Are you sure you want to delete this link? This action can not be undone.\');">'
                            +  '<input type=hidden value="' + data + '" name="link_token">'
                            +      '<button type="submit" class="btn btn-default" title="delete link">'
                            +          '<i class="fal fa-trash" aria-hidden="true"></i>'
                            +      '</button>'
                            + '</form>'
                }
            }
        ],
        "initComplete": function() {
            // Instantiate clipboard button event listeners after data draw so that we capture all the copy buttons
            new Clipboard('.copy-button');
        }
    });

    // deselect buttons after clicking
    $(".btn").mouseup(function(){
        $(this).blur();
    });

});    // Close document.ready