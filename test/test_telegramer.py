
import sys, os

from core.telegramer import delete_media_host


def test_delete_media_host():
	a1 = delete_media_host('J. Cole | @billboardchartsTM o - Snow On Tha Bluff')
	assert  a1 == 'J. Cole - Snow On Tha Bluff'

	a2 = delete_media_host('City Girls - Enough/Better')
	assert a2 == 'City Girls - Enough-Better'

	a3 = delete_media_host('Leil Lowndes - Trick 26 - How to Be a "You-Firstie" to Gain Their Respect and Affection')
	assert a3 == "Leil Lowndes - Trick 26 - How to Be a 'You-Firstie' to Gain Their Respect and Affection"

	a4 = delete_media_host('J. Cole - The Climb Back | music.com')
	assert a4 == 'J. Cole - The Climb Back'

	a5 = delete_media_host('Neil Gaiman - The Graveyard Book (3/7)')
	assert a5 == 'Neil Gaiman - The Graveyard Book (3-7)'

	a6 = delete_media_host('Lil Baby - All In | @billboardchartsTM')
	assert a6 == 'Lil Baby - All In'

	a7 = delete_media_host('Artist - Song Title (feat. Artist) | music.com [Prod. by producer] || music.net')
	assert a7 == 'Artist - Song Title (feat. Artist) [Prod. by producer]'

	a8 = delete_media_host('Artist - LEGEND MIXTAPE || music.ng [BBMC- XXX111XXX]')
	assert a8 == 'Artist - LEGEND MIXTAPE'

	a9 = delete_media_host('Follow music.com.ng CEO on IG @XXX111XXX - #music.ng - Best of Artist Dj Name')

	assert a9 == 'Follow CEO on IG - Best of Artist Dj Name'

	a10 = delete_media_host('Artist-name - Song-title - music.com')
	assert a10 == 'Artist-name - Song-title'

	a11 = delete_media_host('SeeB & Skip Marley - Cruel World [music.kz]')
	assert a11 == 'SeeB & Skip Marley - Cruel World'

	a12 = delete_media_host('Leil Lowndes - Trick 32 - How to Sound Like You Know All About Their Job or Hobby')
	assert a12 == 'Leil Lowndes - Trick 32 - How to Sound Like You Know All About Their Job or Hobby'

# TODO add integration test.