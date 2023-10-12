$("#form_filter_items").submit(function() {
    $(this).find(":input").filter(function () {
        return !this.value;
    }).attr("disabled", true);

    return true;
});