/**************************************************************************************************
INDEX JS
**************************************************************************************************/
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom'
import * as serviceWorker from './service-worker';
import App from './app-component';

ReactDOM.render(
	/* must be in this format */
	<BrowserRouter>
		<App />
	</BrowserRouter>, 
	document.getElementById('root')
);

serviceWorker.unregister();
