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
      title: 'Data Science',
      path: '/data-science',
      component: PR.DataScience,
      order: 2,
   },
   {
      title: 'Statistics',
      path: '/statistics',
      component: PR.Statistics,
      order: 3,
   },
]

