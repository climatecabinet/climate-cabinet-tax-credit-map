"use client";

/**
 * A map control panel for GeoJSON data layers and base tilesets.
 */

import Checkbox from "@/components/Checkbox";
import RadioButton from "@/components/RadioButton";
import { useState, useEffect } from "react";
import { useSnapshot } from "valtio";
import { useLayers } from "@/hooks/useLayers";
import { baseMapStore, reportStore, layerStore } from "@/states/search";

function MapControlPanel() {
  const reportSnap = useSnapshot(reportStore);
  const baseMapSnap = useSnapshot(baseMapStore);
  const layerSnap = useSnapshot(layerStore);
  const layerActions = useLayers(reportSnap?.report, layerStore);

  // Intialize panel visiblity
  const [expanded, setExpanded] = useState(true);

  useEffect(() => {
    // Function to check the window's width and update the expanded state
    const updateMenuState = () => {
      const isMobile = window.innerWidth <= 768; // 768px is typically considered the breakpoint for mobile
      setExpanded(!isMobile);
    };

    // Check once on component mount
    updateMenuState();

    // update the state when the window resizes
    window.addEventListener("resize", updateMenuState);
    return () => window.removeEventListener("resize", updateMenuState);
  }, []);

  return (
    <div
      className={`w-full max-w-xs mx-auto px-2 ${
        expanded ? "bg-white" : "bg-transparent"
      }`}
    >
      {/** MENU */}
      <div
        className={`form-control h-0 overflow-hidden items-start ${
          expanded && "h-auto overflow-auto max-h-full"
        }`}
      >
        {/** TITLE */}
        <div className="mx-auto">
          <h5>Select Layers</h5>
        </div>
        {/** SECTION DIVIDER */}
        <div className="divider m-0"></div>

        {/** DATA LAYER CHECKBOXES */}
        {layerActions.getToggleOptions().map((option, index) => {
          return (
            <Checkbox
              key={index}
              option={option}
              checked={layerSnap[option].visible}
              disabled={!layerSnap[option].hasData}
              onChange={(e) => layerActions.toggleLayer(e)}
            />
          );
        })}

        {/** DATA LAYER BULK OPERATION BUTTONS */}
        <div className="flex justify-center mx-auto py-2">
          <button
            className="btn join-item btn-sm normal-case mx-1"
            onClick={(_) => layerActions.showAllLayers()}
          >
            All
          </button>
          <button
            className="btn join-item btn-sm normal-case mx-1"
            onClick={(_) => layerActions.hideAllLayers()}
          >
            None
          </button>
        </div>

        {/** SECTION DIVIDER */}
        <div className="divider m-0"></div>

        {/** BASE MAP RADIO BUTTONS */}
        {Object.entries(baseMapSnap.options).map(
          ([mapType, settings], index) => (
            <RadioButton
              key={index}
              option={mapType}
              name={settings.name}
              isChecked={settings.name == baseMapSnap.selected.name}
              onChange={(e) => baseMapSnap.setMap(e.target.value)}
            />
          )
        )}
      </div>

      {/** MENU TOGGLE BUTTON */}
      {/* <div className="flex justify-center py-2"> */}
      <div
        className={`flex py-2 ${expanded ? "justify-center" : "justify-end"}`}
      >
        <button
          className="btn btn-sm normal-case"
          onClick={() => setExpanded((e) => !e)}
        >
          {expanded ? (
            "Collapse Menu"
          ) : (
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          )}
        </button>
      </div>
    </div>
  );
}

export default MapControlPanel;
