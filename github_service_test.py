# Github Service Test

import unittest
import GitHubService as gs
import os

import requests


class TestGithubService(unittest.TestCase):

	def test_get_repo_url(self):
		headers={'Authorization':'token 5c4d81ec05cb82053d9fd0c0519120fe3eed17be',
        'User-Agent':'https://api.github.com/meta',
        'Content-Type':'application/json'}

		pull_req = requests.get('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:dlew/joda-time-android',headers=headers)
		url = gs.get_repo_url(pull_req)
		self.assertEqual(url,'https://github.com/dlew/joda-time-android')


	"""def test_process(self):
					sha_list = ['3b45f2cad666726f06f14347026cc25a05051246', '65e1cae2decfc1b86481eb40607eac0e23b64b0c', '0b7343dd345f314d02b2c21ea69b84a02ac2c94f', '8b06ea52ab2915725635a5fb34c1468f9787d422', '86ee59c23202692a3d4814e1a7df119c8a1ce430', 'ecad8647035c39dfc068c79c3d026b5fd8c7a50c', 'ac57d67f45c1017b24117ec0dc491787df936a42', '960d2ea6f70d1f38e269e711aff3877c4bb5430c', '87cb33f69b0d612e029ee454253f3a7cbce05fb6', '915a1f3eb0d251cfa9c432cd0a582278f698cd84', '696ed86affe8e04a681d05077877f3f5b8191f09', 'e0b8f6f85059779f80f166305574759cb28488ab', '991ba320a6b2cde1b892e87ebca77be249884560', '522fbc035fe319fbf6fad58579fdf36491babe18', '40e5cc628a1a3f5c53ed006f093fb7cddffd5d54', '7a13012855bcdebb4962e102ed03f08b44a3d095', 'c3b102e547535a5410250b264f35020c176d6e1b', '3f9a5a254ec40b1073f48711f798df5eae3ec45c', '05a9c030c0b8b515ae9ddc71b0a1f0387e49ee3c', '143213483c6e1ba13fa8c1bb2cc5008b7414960e', '678fa93838dd149eac61a71f1a5dee58ddce0584', 'b2607010b4adacb47496fe1981e875fef24d044d', 'b2dd36f607fa0faa69acf6351067077506553a68', 'af6973884f643712a445bcafd0aaee5c8bf2bb2f', '3894a0bb6cdf397ef46fea64fa5516f562bbb8b9', '49f84349117f1370be4a63800f5ca4f3dab07ebc', '7a7ba871dc1250765b1e1804d9abf642497ee6b6', '36f5947cd78a66eeec0b1de51c92100c94b345ad', 'f62ae456b03eea52addb95d8e3bbdf0277632d65', '080571651550af8798e0b36c41043a52121bc763', '9f797b3009e107835717f1afb6cce054ae457dc9', 'e9a541259b8d24726ad26f13df350c5467d63b3b', '9667878b5f3dacb8a9bd1a7c7d95fa13a153b2d5', '4c4cbd41cf8a1310304bd16a2b40acb18ee7a05d', 'f7825f6c9942b0d7e07f500bc8f5b4ebf227a8af', '94fdefee3a65f8a67335c919440c1a8962681c51', 'b61b64073a01edd5fd1154a5993ea028732d4229', '90570f809be327fae1d047b2c621ebaca689693f', 'ed37d5cdc76581a6db2c8dbd00e4b779e8b84eaa', 'e046007db760fcd2c071ba66369a27c1813f59f5', '03061613803ff475ca22d40627f2ea754f6652fb', '6694d742a370e0f181530734481284de8d5dd8ef', '3defc1b36a0f73b4a0be6944846ee02d58e8c86f', '9677cc4eea8186da314cdd2eeb259c513880e1fd', 'fc690869db2ff03e474e2d5112842f40497345fb', '37c9b922a76fcf84b68909a063558dd72c2b96c1', '93c54a2ee563ac1fc6337dd120b667f05b6f72a9', '5a930f6a268f968746662b8e2a91348c4880f063', '235fe6a7ca904be70ebc7e01876b6af456e80d44', '5373214b70db93181b14128ea65b317718940fbf', '2a4edad23ae5ce9af394826ad9354bd36a9e03ab', 'c1ea04e00296273fdc98429913d9c2389b3cde17', '10c0879d3b8fc70fea763ec83a69ecef79c3c009', '620f408688169abea35490263edd0085946e4c9a', '2456b9f4b0a107916aaba97e2e8abab9954fb418', '144db43ad4af09a708ddf53516a5f982d93ceecd', 'f7c396b0fdcb222cb055a36c38d77b6f07691f68', '04f2be64c668762bd505828c730e56d7f48ff9a9', '8312e09f6eab6ca37f11e7f0c534cbc67542d967', '176bb85f404b7140bdec5fda285505f341a079a0', '7e7a0c83f55c0243191d3b5453a3b3e73a3f2ef5', '4dbf646b37ddaec5da26a3892c1374e55b8e4aaa', '506d316529bba49c4ca88897844b0f4b578a832b', '7cf897a051373919da850bf9cb2d87357e61573c', '8a9162f54202a1d086623724dcc9c4c56146f2d0', 'fb64d69347d145a8b1cd683d0aa8c3d728f4408c', '5c953d7d005551352d5c7b1d76d77f18037a5def', '14279278cd2c57942af6effd2e0126badfc74133', '933c84ff1c82ee4c0e3faa147f6160380e2bb817', '3634b3338cc2fab6cfa147c9475b986165471b73', 'd37922bf823900f9ce319736927dfb2203808ded', '87ee97a1126b170b764eca90787ca221161706f8', 'c45e9a1faf24dd58929b957b7b3e3f4c8ca8de04', '6e0bf59e5a7e2a768f0ddc923178e8153ba3c0ce', 'a2a13758e0abfaa23f74f473314214f3f1bec7cf', 'eeaf7e4b7c1b60b4ab251a5eb3ce2847c59b36cd', '89bfaf876eb97aaefd4f632d0fe130983c33b638']
					gs.clone_repo('https://github.com/iluwatar/java-design-patterns.git','java-design-patterns',1)
					gs.clone_repo('https://github.com/iluwatar/java-design-patterns.git','java-design-patterns',2)
					num = gs.process(sha_list,'java-design-patterns','D:\\code\\java-design-patterns\\1','D:\\code\\java-design-patterns\\2',3)
					if num < 1:
						self.fail('Number of projects cannot be less than 1')"""

	def test_clone_repo(self):

		dir = gs.clone_repo('https://github.com/dlew/joda-time-android.git','joda-time-android',1)
		if not os.path.isdir(dir):
			self.fail("Repo Clone test failed")


	def test_get_pull_req(self):
		headers={'Authorization':'token 5c4d81ec05cb82053d9fd0c0519120fe3eed17be',
        'User-Agent':'https://api.github.com/meta',
        'Content-Type':'application/json'}

		pull_req = requests.get('https://api.github.com/search/issues?q=type:pr+language:java+state:closed+is:merged+status:success+repo:dlew/joda-time-android',headers=headers)

		commit_list = gs.get_pull_req(pull_req)
		if len(commit_list) < 1:
			self.fail('Commit list for pull request is empty')


if __name__ == '__main__':
	unittest.main()
