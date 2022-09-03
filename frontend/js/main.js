import React from 'react';
import {render} from 'react-dom';
import ListItem from "./components/list-item";


const App = () => {
    return (
        <div>
            <div>
                <div className="py-16 px-8">

                    <div className="border border-gray-300 rounded bg-white shadow-md">
                        <form>
                            <div className="flex items-center pl-12 pr-6 py-5">

                                <label htmlFor="short-url" className="text-2xl font-normal tracking-tight mr-6 opacity-80">URL:</label>
                                <input id="short-url" className="flex-grow mr-4" type="text" placeholder="https://" />
                                    <button className="button button-green font-base px-8 py-2" type="submit">
                                        <span>Shorten</span>
                                    </button>

                            </div>
                        </form>
                    </div>

                    <div className="mt-24 mb-20">
                        <p className="text-white text-center text-4xl">Your shortened links will appear here</p>
                    </div>

                </div>
            </div>
            <ListItem />
        </div>
    )
}

render(<App />, document.getElementById('app-root'));
