// SETUP CODE FOR THE SEARCHING FEATURE

var searchInput = document.getElementById('searchInput');
var searchDropdown = document.getElementById('searchDropdown');

var maxHeight = window.innerHeight - 100;

// Set initial max-height of the dropdown menu
$('#searchDropdown').css({
    'max-height': maxHeight + 'px'
});

// Update the dropdown menu max-height when the window is resized
$(window).on('resize', function () {
    $('#searchDropdown').css({
        'max-height': maxHeight + 'px'
    });
});

// Toggle the dropdown menu when clicking the search box
searchInput.addEventListener('click', function () {
    $('#searchDropdown').toggle();
});

// Close the dropdown when clicking outside
$(document).on('click', function (event) {
    var target = $(event.target);
    if (!target.closest('.dropdown').length) {
        $('#searchDropdown').hide();
    }
});

searchInput.addEventListener('input', function () {
    var searchText = searchInput.value.trim();
    console.log(searchText);
    if (searchText === '') {
        searchDropdown.innerHTML = '';
        searchDropdown.style.display = 'none';
        return;
    }

    // Send an AJAX request to the server to fetch the search results
    $.ajax({
        url: '/search',
        method: 'GET',
        data: { query: searchText },
        success: function (response) {
            // Update the dropdown list with the search results
            searchDropdown.innerHTML = response;
            searchDropdown.style.display = 'block';

            // Update the dropdown menu width after updating the content
            searchDropdown.style.width = searchInput.offsetWidth + 'px';

            // Adjust the max-height of the dropdown menu if needed
            if (searchDropdown.scrollHeight > maxHeight) {
                searchDropdown.style.overflowY = 'scroll';
            } else {
                searchDropdown.style.overflowY = 'auto';
            }
        },
        error: function (error) {
            console.error(error);
        }
    });
});
