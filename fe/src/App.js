import { CssBaseline, ThemeProvider } from "@mui/material";
import { useSelector } from "react-redux";
import { Route, Routes } from "react-router-dom";
import Topbar from "./components/global/Topbar";
import Graph from "./scenes/graph";
import LoginPage from "./scenes/login";
import Portfolio from "./scenes/porfolio";
import RegisterPage from "./scenes/register";
import Trades from "./scenes/trades";
import { ColorModeContext, useMode } from "./theme";
import PrivateRoute from "./utils/PrivateRoute";

function App() {
  const [theme, colorMode] = useMode();
  const isLoggedIn = useSelector(state => state.auth.isLoggedIn)
  console.log(isLoggedIn)

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <main className="content">
            {
              isLoggedIn ? <Topbar />:<></>
            }
            <Routes>
              <Route element={<PrivateRoute />}>
                <Route path='/' element={<></>} />
                <Route path="/trades" element={<Trades />} />
                <Route path="/portfolio" element={<Portfolio />} />
                <Route path='/graph' element={<Graph />}/>
              </Route>
              <Route element={<LoginPage />} path="/login" />
              <Route element={<RegisterPage />} path="/register" />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
