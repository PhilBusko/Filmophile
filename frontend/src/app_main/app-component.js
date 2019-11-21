/**************************************************************************************************
APP-COMPONENT
**************************************************************************************************/
import * as React from 'react';
import { Switch, Route } from 'react-router-dom'
import { RoutesConfig } from './routes'
import './styles.scss'

class App extends React.Component {
   render() {  
      return (
         <Switch> 
            { 
               RoutesConfig.map( ({path, component}, key) => 
                  <Route exact path={ path } component={ component } key={ key } /> )
            }
         </Switch>
      );
   }
}

export default App;
