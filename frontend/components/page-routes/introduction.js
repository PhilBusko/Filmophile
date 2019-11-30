/**************************************************************************************************
HOME PAGE
**************************************************************************************************/
import React, { Component } from 'react';

import MenuLayout from '../layouts/menu-layout'
import ResourceLink from '../elements/resource-link'

class Introduction extends Component {

    moviedbIcon = require('../assets/icons/moviedb.svg')
    reelgoodIcon = require('../assets/icons/reelgood.png')
    imdbIcon = require('../assets/icons/imdb.ico')
    jupyterIcon = require('../assets/icons/jupyter.png')
    pandasIcon = require('../assets/icons/pandas.png')
    seleniumIcon = require('../assets/icons/selenium.ico')
    sklearnIcon = require('../assets/icons/sklearn.ico')
    djangoIcon = require('../assets/icons/django.png')
    postgresIcon = require('../assets/icons/postgres.png')
    reactIcon = require('../assets/icons/react.ico')
    sassIcon = require('../assets/icons/sass.png')
    purecssIcon = require('../assets/icons/purecss.png')
    webpackIcon = require('../assets/icons/webpack.ico')
    githubIcon = require('../assets/icons/github.png')

    render() {
        return (
            <MenuLayout>
                <div className='pure-g'>

                    <div className='pure-u-1 page-title grid-spacing'>
                        <div className=''>
                            Phil-mo-phile
                        </div>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        Welcome to Phil's Filmophile site. 
                        The goal of this site is to aggregate movies and TV shows from different streaming sources
                        and make them available in one place. 
                        The site was first built for the&nbsp;
                        <a className='link-format' href='https://flatironschool.com/' target='blank_'
                            style={{'display': 'contents'}}>FlatIron School's</a>
                        &nbsp;Data Science Bootcamp,
                        but it is a dear project to me, and has been expanded since.
                        The site also features a recommendation system which is unlike anything else available
                        on the market.
                        Credit is given to the following resources:
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <div className='left-panel'>
                            <span className='entry-title'>Data Sources:</span> 
                            <span>
                                <ResourceLink url={'https://www.themoviedb.org'} 
                                    icon={ this.moviedbIcon } text='TMDB'></ResourceLink>
                                <ResourceLink url={'https://reelgood.com/'} 
                                    icon={ this.reelgoodIcon } text='Reelgood'></ResourceLink>
                                <ResourceLink url={'https://www.imdb.com/'} 
                                    icon={ this.imdbIcon } text='IMDB' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <div className='left-panel'>
                            <span className='entry-title'>Data Science:</span> 
                            <span>
                                <ResourceLink url={'https://jupyter.org/'} 
                                    icon={ this.jupyterIcon } text='Jupyter Project'></ResourceLink>
                                <ResourceLink url={'https://pandas.pydata.org/'} 
                                    icon={ this.pandasIcon } text='pandas'></ResourceLink>
                                <ResourceLink url={'https://selenium.dev/'} 
                                    icon={ this.seleniumIcon } text='Selenium'></ResourceLink>
                                <ResourceLink url={'https://scikit-learn.org/stable/'} 
                                    icon={ this.sklearnIcon } text='scikit-learn'></ResourceLink>
                                <ResourceLink url={'https://www.imdb.com/'} 
                                    icon={ this.sklearnIcon } text='plot.ly' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <div className='left-panel'>
                            <span className='entry-title'>Backend:</span> 
                            <span>
                                <ResourceLink url={'https://www.djangoproject.com/'} 
                                    icon={ this.djangoIcon } text='Django'></ResourceLink>
                                <ResourceLink url={'https://www.postgresql.org/'} 
                                    icon={ this.postgresIcon } text='PostgreSQL' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <div className='left-panel'>
                            <span className='entry-title'>Frontend:</span> 
                            <span>
                                <ResourceLink url={'https://reactjs.org/'} 
                                    icon={ this.reactIcon } text='React'></ResourceLink>
                                <ResourceLink url={'https://sass-lang.com/'} 
                                    icon={ this.sassIcon } text='Sass'></ResourceLink>
                                <ResourceLink url={'https://purecss.io/'} 
                                    icon={ this.purecssIcon } text='Pure.css'></ResourceLink>
                                <ResourceLink url={'https://webpack.js.org/'} 
                                    icon={ this.webpackIcon } text='webpack' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <div className='left-panel'>
                            <span className='entry-title'>Deployment:</span> 
                            <span>
                                <ResourceLink url={'https://github.com/PhilBusko/Filmophile'} 
                                    icon={ this.githubIcon } text='Github Repo'></ResourceLink>
                                <ResourceLink url={'https://github.com/PhilBusko/Filmophile'} 
                                    icon={ this.githubIcon } text='PaaS' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                    </div>

                </div>
            </MenuLayout>
        ); }
    }

export default Introduction;
