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
        return Math.ceil(pageCount);
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
                    pageCount={ this.getPageCount() }
                    pageRangeDisplayed={ 2 }
                    marginPagesDisplayed={ 1 } 
                    onPageChange={ this.handlePageClick }

                    containerClassName={ 'paginate-panel' }
                    pageLinkClassName={ 'center-both page-class' }
                    activeLinkClassName={ 'active' }
                    breakLinkClassName={ 'break-me center-both control-class' }

                    previousClassName={ 'center-both ' }
                    previousLinkClassName={ 'control-class' }
                    nextClassName={ 'center-both ' }
                    nextLinkClassName={ 'control-class' }

                    previousLabel={ '<<' }
                    nextLabel={ '>>' }
                    breakLabel={ '...' }
                />
            </div>
        );
    }
}

export default Paginator;
export { PERPAGE };

