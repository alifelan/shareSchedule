function filter() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searched");
  filter = input.value.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, "");
  data = document.getElementById("classes");
  class_ = data.getElementsByTagName("p");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < class_.length; i++) {
    if (class_) {
      txtValue = class_[i].textContent.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, "");
      if (txtValue.indexOf(filter) > -1) {
        class_[i].style.display = "";
      } else {
        class_[i].style.display = "none";
      }
    }
  }
}
