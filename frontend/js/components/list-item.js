import React, {useState} from 'react';

const ListItem = () => {
    const [expanded, setExpanded] = useState(false);


    return (
        <div className="mb-6 px-8">

            <div className="border border-gray-300 rounded bg-white shadow-md">
                <div className="flex justify-between items-center pl-12 pr-6 py-4">

                    <div className="text-2xl font-normal tracking-tight opacity-80">
                        That cool document
                    </div>

                    <div className="text-2xl font-normal tracking-tight opacity-80">
                        <a href="#">l.campen.co/Be4df88a</a>
                    </div>

                    <div className="flex items-center">
                        <div>
                            <button className="circle-button border mr-2">C</button>
                        </div>

                        <div>
                            <button className="circle-button" onClick={ () => setExpanded(!expanded) }>
                                …
                            </button>
                        </div>
                    </div>

                </div>
            </div>

            {expanded &&
                <div
                    className="border-l border-r border-b border-gray-300 rounded-b bg-gray-100 bg-opacity-90 border-t border-gray-300">
                    <div className="flex justify-between pl-12 pr-6 py-8">

                        <div>
                            <div className="mb-4">
                                <div className="text-sm uppercase font-bold mb-2">
                                    Name
                                </div>
                                <div className="text-lg font-base">
                                    That cool document
                                </div>
                            </div>
                            <div>
                                <div className="text-sm uppercase font-bold mb-2">
                                    URL
                                </div>
                                <div className="text-lg font-base">
                                    https://www.google.com/?search=this+cool+document+i+found
                                </div>
                            </div>
                        </div>

                        <div>
                            <div className="text-sm uppercase font-bold mb-2">
                                Created
                            </div>
                            <div className="text-lg font-base">
                                2 minutes ago
                            </div>
                        </div>

                        <div className="flex items-end">
                            <div>
                                <button className="circle-button border mr-2">C</button>
                            </div>

                            <div>
                                <button className="circle-button">X</button>
                            </div>
                        </div>

                    </div>
                </div>

            }

        </div>
    )
}

export default ListItem;
