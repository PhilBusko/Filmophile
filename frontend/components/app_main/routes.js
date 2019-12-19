/**************************************************************************************************
APP-MAIN ROUTES
**************************************************************************************************/
import * as PR from '../page-routes/_index.js'

export const RoutesConfig = [
    {
        title: 'Recommended',
        path: '/recommended-movies',
        component: PR.BrowseToWatch,
        order: 1,
    },
    {
        title: 'Watched',
        path: '/watched-movies',
        component: PR.BrowseWatched,
        order: 2,
    },
    {
        title: 'Exploration',
        path: '/exploration',
        component: PR.Exploration,
        order: 3,
    },
    {
        title: 'Data Science',
        path: '/data-science',
        component: PR.DataScience,
        order: 4,
    },
    {
        title: 'About',
        path: '/about',
        component: PR.About,
        order: 5,
    },
    {
        title: 'Admin',
        path: '/admin',
        component: PR.Admin,
        order: 10,
    },
]

