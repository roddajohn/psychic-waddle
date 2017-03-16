$(document).ready(function() {
    $('button[data-confirm]').click(function(ev) {
	var href = $(this).attr('href');
	$('#dataConfirmModal').find('.modal-body').text($(this).attr('data-confirm'));
	$('#dataConfirmOK').attr('href', href);
	$('#dataConfirmModal').modal({show:true});
	return false;
    });
});

$(document).ready(function() {
    $('a[data-confirm]').click(function(ev) {
	var href = $(this).attr('href');
	$('#dataConfirmModal').find('.modal-body').text($(this).attr('data-confirm'));
	$('#dataConfirmOK').attr('href', href);
	$('#dataConfirmModal').modal({show:true});
	return false;
    });
});
