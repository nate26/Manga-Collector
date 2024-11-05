defmodule MangaServiceWeb.VolumesController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.VolumesDB

  def index(conn, _params) do
    volumes = VolumesDB.list_volumes_in_series(conn.params["series_id"], conn.params["limit"], conn.params["offset"])
    render(conn, :index, volumes: volumes)
  end

  def show(conn, %{"isbn" => isbn}) do
    volume = VolumesDB.get_volume_by_isbn!(isbn)
    render(conn, :show, volume: volume)
  end
end
