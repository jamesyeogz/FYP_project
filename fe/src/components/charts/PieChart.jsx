import { Box, useTheme } from '@mui/material'
import { ResponsivePie } from '@nivo/pie'
import React from 'react'
import { tokens } from '../../theme';


const PieChart = () => {
const theme = useTheme();
const colors = tokens(theme.palette.mode)
const data= [
    {
      "id": "Profit",
      "label": "Profit",
      "value": 1007,
      "color": colors.greenAccent[500]
      
    },
    {
      "id": "Loss",
      "label": "Loss",
      "value": 500,
      "color": colors.redAccent[500]
    },
  ]
  return (
    <Box maxHeight={200} width={200}>
    <ResponsivePie
    data={data}
    margin={{top:40,bottom:40,left:40,right:40}}
    innerRadius={0.6}
    colors={{ datum: 'data.color' }}
    padAngle={4}
    arcLinkLabelsDiagonalLength={5}
    arcLinkLabelsStraightLength={5}
    arcLinkLabelsTextColor={colors.primary[100]}
    />
    </Box>

  )
}

export default PieChart