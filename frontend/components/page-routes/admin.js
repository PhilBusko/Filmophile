/**************************************************************************************************
ADMIN PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';

import MenuLayout from '../layouts/menu-layout'
import { SelectWrapper} from '../elements'

class Admin extends React.Component {

    state = {
    }

    componentDidMount() {
        axios({
            url: 'api/movies/recom_levels/',
        }).then( success => {
            this.setState({ recomLevels: success.data });
        }).catch( error => {
            console.log('Axios Error: api/movies/recom_levels/')
            console.log(error);
        });
    }

    render() {
        return (
            <MenuLayout>
                <div className='pure-g spacing-outer'>
                    <div className='pure-u-1'>
                        <div className='spacing-inner page-title'>
                            Webmaster Dashboard
                        </div>
                    </div>

                    <div className='pure-u-1-3'>
                        <div className='spacing-inner control-island control-outer'>

                            <div className='control-inner'>
                                ctrl
                            </div>

                            <div className='control-dummy'>
                            </div>

                        </div>
                    </div>
                </div>
            </MenuLayout>
        );
    }
}

export default Admin;
