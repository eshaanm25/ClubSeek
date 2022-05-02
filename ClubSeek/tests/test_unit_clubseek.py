import clubseek.main
import clubseek.helpers

def test_bar_greatest():
    allBarObjects = []
    allBarObjects.append(
        clubseek.main.Bars(
            address = "cheese",
            barName = "pizza",
            capacity = 365,
            currentTraffic = 12,
            wowFactor = 88
        )
    )
    
    allBarObjects.append(
        clubseek.main.Bars(
            address = "pizza",
            barName = "cheese",
            capacity = 365,
            currentTraffic = 12,
            wowFactor = 77
        )
    )

    greatestBar = clubseek.helpers.getGreatestWow(allBarObjects)

    assert greatestBar.address == "cheese"


