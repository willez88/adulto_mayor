/**
 * @brief Función que agrega los botones para exportar en un dataTable
 * @param tabla dataTable al cual se le agregan los botones
 */
function button_datatable(table) {
    new $.fn.dataTable.Buttons(table, {
        buttons: [
            {
                extend: 'copyHtml5',
            },
            {
                extend: 'csvHtml5',
                fieldBoundary: '',
                fieldSeparator: ';',
                title: 'adulto_mayor',
            },
            {
                extend: 'excelHtml5',
                title: 'adulto_mayor',
            },
            {
                extend: 'pdfHtml5',
                title: 'adulto_mayor',
            },
            {
                extend: 'print',
            },
        ],
      });
      table.buttons().container().appendTo(table.table().container());
}
