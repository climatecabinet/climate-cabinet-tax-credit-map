"use client";

/***
 * A parent container for a DeckGL map and control panel.
 */

import "mapbox-gl/dist/mapbox-gl.css";
import MapNotification from "@/components/MapNotification";
import MapControlPanel from "@/components/MapControlPanel";
import { MapboxOverlay } from "@deck.gl/mapbox";
import Tooltip from "@/components/Tooltip";
import { Map, useControl, FullscreenControl } from "react-map-gl";
import { useSnapshot } from "valtio";
import { useRef, useEffect } from "react";
import {
  reportStore,
  baseMapStore,
  viewportStore,
  layerStore,
} from "@/states/search";
import { useLayers } from "@/hooks/useLayers";

function DeckGLOverlay(props) {
  const overlay = useControl(() => new MapboxOverlay(props));
  overlay.setProps(props);
  return null;
}

function MapWidget() {
  const reportSnap = useSnapshot(reportStore);
  const baseMapSnap = useSnapshot(baseMapStore);
  const layerSnap = useSnapshot(layerStore);
  const layerClient = useLayers(reportSnap?.report, layerStore);
  const mapRef = useRef(null);

  const layers = Object.entries(layerSnap).reduce((layers, [id, state]) => {
    if (state.visible) {
      let lyr = layerClient.getLayer(id);
      layers.push(lyr);
    }
    return layers;
  }, []);

  const flyToLocation = (lat, lon, z) => {
    if (!mapRef.current) return;
    const map = mapRef.current;
    map.flyTo({
      center: [lon, lat],
      zoom: z,
    });
  };

  useEffect(() => {
    flyToLocation(
      viewportStore.current.latitude,
      viewportStore.current.longitude,
      viewportStore.current.zoom
    );
  }, [viewportStore.current]);

  return (
    <div
      className="relative overflow-hidden"
      style={{ width: "100%", height: "100%" }}
    >
      <Map
        mapStyle={baseMapSnap.selected.url}
        mapboxAccessToken={process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN}
        projection="mercator"
        initialViewState={viewportStore.current}
        controller={true}
        ref={mapRef}
        dragRotate={false}
      >
        <FullscreenControl position="top-left" containerId="report-widget" />
        <DeckGLOverlay layers={layers} interleaved={true} />
      </Map>
      <Tooltip />
      <div className="absolute right-4 top-4 p-2">
        <MapControlPanel
          baseMapSnap={baseMapSnap}
          reportSnap={reportSnap?.report}
          layerStore={layerStore}
        />
      </div>
      {/* Conditionally display loading banner */}
      {reportSnap.status && !reportSnap.status.includes("success") ? (
        <div className="absolute top-0 left-0 w-full h-full bg-opacity-50 bg-black flex items-center justify-center z-50">
          <MapNotification notificationText={"Loading geographies..."} />
        </div>
      ) : null}
    </div>
  );
}

export default MapWidget;
