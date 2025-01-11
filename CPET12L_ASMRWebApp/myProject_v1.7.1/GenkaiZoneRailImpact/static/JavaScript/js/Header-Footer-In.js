function handleIconClick(page) {
    switch (page) {
        case 'Profile':
            window.location.href = profileUrl;
            break;
        case 'Menu':
            window.location.href = menuUrl;
            break;
        case 'Cart':
            window.location.href = cartUrl;
            break;
        default:
            break;
    }
}
