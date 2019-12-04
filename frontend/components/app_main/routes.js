/**************************************************************************************************
APP-MAIN ROUTES
**************************************************************************************************/
import * as PR from '../page-routes/_index.js'

export const RoutesConfig = [
    {
        title: 'Introduction',
        path: '/',
        component: PR.Introduction,
        order: 1,
    },
    {
        title: 'Exploration',
        path: '/exploration',
        component: PR.Exploration,
        order: 2,
    },
    {
        title: 'Data Science',
        path: '/data-science',
        component: PR.DataScience,
        order: 3,
    },
    {
        title: 'To Watch',
        path: '/browse-to-watch',
        component: PR.BrowseToWatch,
        order: 4,
    },
    {
        title: 'Watched',
        path: '/browse-watched',
        component: PR.BrowseWatched,
        order: 5,
    },
]

