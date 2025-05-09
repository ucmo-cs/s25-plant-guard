import { Link } from "react-router-dom";
import { Sidebar, SidebarItems, SidebarItemGroup, SidebarItem } from "flowbite-react";

export default function AppSidebar() {
  return (
    <Sidebar aria-label="Pi Sidebar">
      <SidebarItems>
        <SidebarItemGroup>
          <Link to="/">
            <SidebarItem>Dashboard</SidebarItem>
          </Link>
          <Link to="/pi/raspPi1">
            <SidebarItem>IoT 1</SidebarItem>
          </Link>
          <Link to="/pi/raspPi2">
            <SidebarItem>IoT 2</SidebarItem>
          </Link>
        </SidebarItemGroup>
      </SidebarItems>
    </Sidebar>
  );
}
