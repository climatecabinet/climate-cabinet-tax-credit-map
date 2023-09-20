/**
 * An autocomplete search bar.
 */

"use client";
import { useCallback } from "react";
import Dropdown from "@/components/Dropdown";
import classNames from "classnames";
import { memo, useState, Suspense } from "react";
import { useSnapshot } from "valtio";
// import { debounce } from "@/lib/utils";
import debounce from "lodash/debounce";
import { searchStore } from "@/states/search";

function Autocomplete() {
  const [innerValue, setInnerValue] = useState("");
  // Initialize visiblity of search results dropdown
  const [open, setOpen] = useState(false);

  // Define function to collapse search results and update selection on click
  const handleClick = (geo) => {
    setOpen(false);
    searchStore.setQuery(geo.name);
    searchStore.setSelected(geo);
  };

  // Take snapshot of state for rendering
  const snap = useSnapshot(searchStore);

  const handleSearch = useCallback(
    debounce((value) => {
      // Do something with the search term
      searchStore.setQuery(value);
    }, 500),
    []
  );

  const handleTextInput = (e) => {
    setInnerValue(e.target.value);
    handleSearch(e.target.value);
  };

  return (
    <div
      className={classNames({
        "dropdown w-full": true,
        "dropdown-open": open,
      })}
    >
      <div>
        <span className="absolute inset-y-0 left-0 flex items-center pl-2">
          <button className="p-1 focus:outline-none focus:shadow-outline bg-white border-white">
            <svg
              fill="none"
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              className="w-6 h-6"
            >
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </span>
        <input
          type="search"
          value={innerValue}
          className="input input-bordered w-full pl-10"
          onChange={handleTextInput}
          placeholder="Type something..."
          tabIndex={0}
        />
      </div>
      <Suspense>
        <Dropdown
          snap={snap}
          handleClick={handleClick}
          nullMessage={"No results found."}
        />
      </Suspense>
    </div>
  );
}

export default memo(Autocomplete);
