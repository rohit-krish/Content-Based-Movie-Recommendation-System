$(document).ready(function () {
    var searchInput = document.getElementById('searchInput');
    var searchDropdown = document.getElementById('searchDropdown');

    var animationDuration = 200;
    var maxWidth = 300;
    var maxHeight = window.innerHeight - 100;

    // Set the initial width of the input element
    var initialWidth = $('#searchInput').outerWidth();
    $('#searchInput').css('width', '100%');

    // Increase the input width to the maximum when clicked
    $('#searchInput').on('click', function () {
        $(this).animate({ width: maxWidth }, {
            duration: animationDuration,
            progress: function () {
                // Update the dropdown menu width during the animation
                searchDropdown.style.width = searchInput.offsetWidth + 'px';
            }
        });
    });

    // Set initial width and max-height of the dropdown menu
    $('#searchDropdown').css({
        width: $('#searchInput').outerWidth(),
        'max-height': maxHeight + 'px'
    });

    // Update the dropdown menu width and max-height when the window is resized
    $(window).on('resize', function () {
        $('#searchDropdown').css({
            width: $('#searchInput').outerWidth(),
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

            // Reset the input width when clicking outside
            $('#searchInput').animate({ width: initialWidth }, animationDuration, function () {
                // Reset the dropdown menu width after the animation
                searchDropdown.style.width = searchInput.offsetWidth + 'px';
            });
        }
    });

    searchInput.addEventListener('input', function () {
        var searchText = searchInput.value.trim();
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
});
