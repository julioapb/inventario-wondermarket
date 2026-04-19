$(document).ready(function(){

  $('#producto_simple').hide()
  $('#producto_combo').hide()

  $('#btn_producto_simple').click(function(){
    $('#producto_simple').show()
    $('#producto_combo').hide()
  });

  $('#btn_producto_multiple').click(function(){
    $('#producto_simple').hide()
    $('#producto_combo').show()
  });
  

    $("#btn_p").click(function(){

          if($('#proveedor').val() == ''){
            alert('Debe inndicar un proveedor');
            return false;
          }

          if($('#precio').val() == ''){
            alert('Debe inndicar un precio');
            return false;
          }

        $.ajax({
				type: "POST",
				url: '/ajax-proveedor',
				data: $("#form_proveedor").serialize(), // Adjuntar los campos del formulario enviado.
				success: function(response)
				{
				
                    //console.log(response)
                
          $("#respuesta").html('Proveedor Guardado Correctamente'); // Mostrar la respuestas del script PHP.
          $('#form_proveedor').reset();
				}
				});
				 return false; // Evitar ejecutar el submit del formulario.
    })

    //ELIMINAR PROVEEDOR
    $("#btn_delete_proveedor").click(function(){

    $.ajax({
      type: "POST",
      url: '/delete_proveedor',
      //data: $("#form_proveedor").serialize(), // Adjuntar los campos del formulario enviado.
      success: function(response)
      {
              //console.log(response)
        $("#respuesta_delete").html('Proveedor Eliminado Correctamente'); // Mostrar la respuestas del script PHP.
        window.history.back();
        location.reload();
      }
      });
      return false; // Evitar ejecutar el submit del formulario.
    })
    //FIN ELIMINAR PROVEEDOR

     //REFRESCAR PAGINA
     $("#btn_r").click(function(){

    
          location.reload();
        
        return false; // Evitar ejecutar el submit del formulario.
      })
      //FIN REFRESCAR PAGINA

        
        $("#add").click(function() {
          var intId = $("#buildyourform div").length + 1;
          var fieldWrapper = $("<div class=\"fieldwrapper\" id=\"field" + intId + "\"/>");
          var fName = $("<input type=\"text\" class=\"fieldname\" />");
          var fType = $("<select class=\"fieldtype\"><option value=\"checkbox\">Checked</option><option value=\"textbox\">Text</option><option value=\"textarea\">Paragraph</option></select>");
          var removeButton = $("<input type=\"button\" class=\"remove\" value=\"-\" />");
          removeButton.click(function() {
              $(this).parent().remove();
          });
          fieldWrapper.append(fName);
          fieldWrapper.append(fType);
          fieldWrapper.append(removeButton);
          $("#buildyourform").append(fieldWrapper);
      });
      $("#preview").click(function() {
          $("#yourform").remove();
          var fieldSet = $("<fieldset id=\"yourform\"><legend>Your Form</legend></fieldset>");
          $("#buildyourform div").each(function() {
              var id = "input" + $(this).attr("id").replace("field","");
              var label = $("<label for=\"" + id + "\">" + $(this).find("input.fieldname").first().val() + "</label>");
              var input;
              switch ($(this).find("select.fieldtype").first().val()) {
                  case "checkbox":
                      input = $("<input type=\"checkbox\" id=\"" + id + "\" name=\"" + id + "\" />");
                      break;
                  case "textbox":
                      input = $("<input type=\"text\" id=\"" + id + "\" name=\"" + id + "\" />");
                      break;
                  case "textarea":
                      input = $("<textarea id=\"" + id + "\" name=\"" + id + "\" ></textarea>");
                      break;    
              }
              fieldSet.append(label);
              fieldSet.append(input);
          });
          $("body").append(fieldSet);
      });

      var maxField = 10; //Input fields increment limitation
      var addButton = $('.add_button'); //Add button selector
      var wrapper = $('.field_wrapper'); //Input field wrapper
      var fieldHTML = "<div><input type='text' name='field_name' value='' class='form-control'/><a href='javascript:void(0);' class='remove_button' title='Remove field'><img src='static/remove-icon.png' width='20opx'/></a></div>"; //New input field html 
      var x = 1; //Initial field counter is 1
      $(addButton).click(function(){ //Once add button is clicked
          if(x < maxField){ //Check maximum number of input fields
              x++; //Increment field counter
              $(wrapper).append(fieldHTML); // Add field html
          }
      });
      $(wrapper).on('click', '.remove_button', function(e){ //Once remove button is clicked
          e.preventDefault();
          $(this).parent('div').remove(); //Remove field html
          x--; //Decrement field counter
      });


});

function actualizarValorMunicipioInm() {
    let municipio = document.getElementById("sku_padre").value;
    //Se actualiza en municipio inm
    document.getElementById("sku_indivisible_2").value = municipio;
}

//controlador buscar producto por sku
function productosSku() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }


//controlador buscar producto por sku indivisible
  function productosSkuIndivisible() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput2");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

  //controlador buscar producto por sku invenrario general
function inventarioGeneral() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput3");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable3");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

  //controlador buscar producto por NOMBRE invenrario general
  function inventariNombre() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput4");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable3");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

 //controlador buscar producto por vencimiento en producto
 function productosVencimiento() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput4");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[7];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

//controlador buscar producto por NOMBRE en producto
function productosnombre() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput5");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[3];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

//controlador buscar producto por PRECIO en producto
function productosprecio() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput7");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[5];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}


//controlador buscar producto por PROVEEDOR en producto
function productosproveedor() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput6");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[8];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

//controlador buscar combos
function combos() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myCombos");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

/* FILTROS GESTION CARGAS */
function estado() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myEstados");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[10];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

function fecha() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myFecha");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[8];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

function order_id() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myOrderid");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

function sku() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("mySku");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

function skuindivisible() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("mySkuindivisible");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[11];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

function nombre() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myNombre");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[13];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}


/* FIN FILTROS GESTION CARGAS */

  function cancelaciones() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

  (function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();

  

  

  