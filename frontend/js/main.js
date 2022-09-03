import React from 'react';
import {render} from 'react-dom';
import ListItem from "./components/list-item";
import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient()


const getLinks = () => {
    return fetch('http://localhost:5011/api/v1.0/links/')
        .then((response) => response.json())
}


const Main = () => {

    const query = useQuery(['links'], getLinks)

    window.data = query.data;

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
            {query.data?.map(link => (
              <ListItem link={ link }/>
            ))}
        </div>
    )
}


const App = () => {
    return (
        <QueryClientProvider client={queryClient}>
            <Main />
            {/* the devtool doesn't render... why not? */}
            <ReactQueryDevtools initialIsOpen={true} position='top-right' />
        </QueryClientProvider>
    )
}

render(<App />, document.getElementById('app-root'));
