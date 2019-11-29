/**************************************************************************************************
RULES-LOADER PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';

import MenuLayout from '../layouts/menu-layout'
import TableWrapper from '../elements/table-wrapper'

class DataScience extends React.Component {

    state = {
        dataHistory: [],
    }

    componentDidMount() {
        axios({
            url: 'api/movies/data_history/',
            method: 'get',
            data: { }
        }).then( success => {
            console.log(success.data);

            let updateState = {dataHistory: success.data};
            this.setState({...this.state, ...updateState});
        }).catch( error => {
            console.log('AXIOS ERROR')
            console.log(error);
        });
    }

    render() {
        return (
            <MenuLayout>
                <div className='pure-g outer-spacing'>

                    <div className='pure-u-1 inner-spacing'>
                        <div className='page-title'>
                            Data Science
                        </div>
                    </div>
                    
                    <div className='pure-u-1 inner-spacing'>
                        <div className=''>

                            <TableWrapper tableRows={ this.state.dataHistory }></TableWrapper>

                        </div>
                    </div>

                </div>
            </MenuLayout>
        );
    }
}

export default DataScience;
