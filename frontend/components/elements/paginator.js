/**************************************************************************************************
PAGINATOR ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
//import { When } from 'react-if';

import ReactPaginate from 'react-paginate';
import './paginator.scss'

const PERPAGE = 40;

class Paginator extends React.Component {

    static propTypes = {
        numberEntries: PropTypes.number.isRequired,  
        updateCurrentPage: PropTypes.func.isRequired,
    }
    
    getPageCount = () => {
        let pageCount = this.props.numberEntries / PERPAGE;
        return pageCount;
    }

    handlePageClick = (data) => {
        const selectedPage = data.selected;
        const offset = selectedPage * PERPAGE;
        this.props.updateCurrentPage(offset);
    }

    render() {
        //console.log(pageCount);

        return (
            <div className='paginator-wrapper'>
                <ReactPaginate
                    onPageChange={ this.handlePageClick }
                    pageCount={ this.getPageCount() }

                    containerClassName={ 'paginate-panel' }
                    activeClassName={ 'active' }
                    breakClassName={ 'break-me' }

                    previousLabel={ 'Prev' }
                    nextLabel={ 'Next' }
                    breakLabel={ '...' }
                    marginPagesDisplayed={ 1 } 
                    pageRangeDisplayed={ 4 }
                />
            </div>
        );
    }
}

export default Paginator;
export { PERPAGE };

