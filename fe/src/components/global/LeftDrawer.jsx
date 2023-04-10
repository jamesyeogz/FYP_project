import {
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import React, { useState } from "react";
import MenuIcon from "@mui/icons-material/Menu";
import { Link } from "react-router-dom";
const LeftDrawer = () => {
  const [drawer, setDrawer] = useState(false);
  const toggleDrawer = () => {
    setDrawer(!drawer);
  };
  return (
    <>
      <IconButton onClick={toggleDrawer}>
        <MenuIcon />
      </IconButton>
      <Drawer
        anchor="left"
        open={drawer}
        onClose={toggleDrawer}
        onClick={toggleDrawer}
      >
        <List>
          <ListItem component={Link} to={"/trades"} sx={{color:'white'}}>
            <ListItemButton>
              <ListItemIcon></ListItemIcon>
              <ListItemText primary={"Trades"} />
            </ListItemButton>
          </ListItem>
          <ListItem component={Link} to={"/portfolio"} sx={{color:'white'}}>
            <ListItemButton>
              <ListItemIcon></ListItemIcon>
              <ListItemText primary={"Porfolio"} />
            </ListItemButton>
          </ListItem>
          <ListItem component={Link} to={"/graph"} sx={{color:'white'}}>
            <ListItemButton>
              <ListItemIcon></ListItemIcon>
              <ListItemText primary={"Graph"} />
            </ListItemButton>
          </ListItem>
        </List>
      </Drawer>
    </>
  );
};

export default LeftDrawer;
