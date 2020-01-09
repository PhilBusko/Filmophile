/**************************************************************************************************
INDEX JS
**************************************************************************************************/
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom'
import * as serviceWorker from './service-worker';
import axios from 'axios';

import App from './app-component';

// set axios defaults
// this isn't best practice - how to configure this for prod ?

axios.defaults.baseURL = 'http://localhost:8000';
//axios.defaults.headers.common['Authorization'] = 'AUTH TOKEN';
axios.defaults.headers.post['Content-Type'] = 'application/json';


ReactDOM.render(
	/* must be in this format */
	<BrowserRouter>
		<App />
	</BrowserRouter>, 
	document.getElementById('root')
);

serviceWorker.unregister();
